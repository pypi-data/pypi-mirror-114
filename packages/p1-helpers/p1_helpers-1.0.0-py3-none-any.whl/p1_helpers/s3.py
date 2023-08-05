"""
Import as:

import p1_helpers.s3 as p1_s3
"""
import datetime
import errno
import io
import logging
import os
import pickle
from typing import Dict, List, Any

import boto3
import botocore
import pandas as pd

import p1_helpers.dbg as p1_dbg
import p1_helpers.io_ as hio

_LOG = logging.getLogger(__name__)
MAX_CHUNK_SIZE = 1000


def is_valid_key(key: str, raise_: bool = False) -> bool:
    """
    Check correctness of s3 key.
    :param key: Path to s3 file
    :param raise_: Raise exception if True
    :return: bool
    """
    result = all(
        (
            not key.startswith("/"),
            not key.startswith("s3://")
        )
    )
    if raise_:
        p1_dbg.dassert(not result,
                    msg=f"file_path shouldn't start with `/` or `s3://` or `/fsx`. "
                        f"key='{key}'")
    return result


def is_key_exists(bucket: str, key: str, raise_: bool = False) -> bool:
    """
    Check whether a object exists on s3.

    :param bucket: the bucket name containing the object
    :param key: s3 key
    :param raise_: raise exception if True
    :return: True if a file exists, False otherwise
    """
    s3 = boto3.client("s3")
    try:
        s3.head_object(Bucket=bucket, Key=key)
        result = True
    except botocore.exceptions.ClientError as error:
        result = False
        if error.response["Error"]["Code"] == "404":
            _LOG.error("File doesn't exists (404). "
                       "bucket='%s', key='%s' exists=%s", bucket, key, result)
        else:
            _LOG.error("File doesn't exists (unhandled response code) "
                       "bucket='%s', key='%s' exists=%s", bucket, key, result)
        if raise_:
            raise error
    _LOG.debug("bucket='%s', key='%s' exists=%s", bucket, key, result)
    return result


def is_prefix_exists(bucket: str, prefix: str, raise_: bool = False) -> bool:
    """
    Check whether something exists in a bucket with provided prefix.
    You can think about it as a check directory exists.

    :param bucket: the bucket name containing the file
    :param prefix: key prefix
    :param raise_: exception if checking the s3 file fails
    :return: True if a file exists, False otherwise
    """
    is_valid_key(prefix, raise_=True)
    s3 = boto3.client("s3")
    result = False
    try:
        response = s3.list_objects(Bucket=bucket, Prefix=prefix, MaxKeys=1)
        if "Contents" in response:
            if len(response["Contents"]):
                result = True
        else:
            result = False

            if raise_:
                _LOG.info("No object with provided prefix were found. "
                          "bucket='%s', prefix='%s' exists=%s", bucket, prefix, result)
                raise FileNotFoundError(
                    errno.ENOENT, os.strerror(errno.ENOENT),
                    f"No object with provided prefix were found. "
                    f"bucket: '{bucket}', prefix: '{prefix}'"
                )
    except botocore.exceptions.ClientError as error:
        result = False
        if error.response["Error"]["Code"] == "404":
            _LOG.error(
                "No object with provided prefix were found (404). "
                "bucket='%s', prefix='%s' exists=%s",
                bucket, prefix, result)
        else:
            _LOG.error("No object with provided prefix were found (Unhandled error code `%s`)."
                       "bucket='%s', prefix='%s' exists=%s",
                       error.response["Error"]["Code"], bucket, prefix, result)
        if raise_:
            raise error
    _LOG.debug("bucket='%s', prefix='%s' exists=%s", bucket, prefix, result)
    return result


def list_keys(s3_bucket: str,
              key_prefix: str,
              chunk_size: int) -> List[str]:
    """
    List s3 keys as a generator.

    A wrapper around `list_objects_v2` method that bypasses its
    restriction for only the first 1000 of the contents.
    Returns only the `Key` fields of the `Contents` field, which contain
    keys.

    `list_objects_v2` returns not only files inside directory but all keys
    with `key_prefix`.

    :param s3_bucket: the name of the bucket
    :param key_prefix: path to the directory that needs to be listed
    :param chunk_size: amount of keys for chunk. Max size AMAZON_MAX_INT.
    :return: list of paths
    """
    is_valid_key(key_prefix, raise_=True)
    p1_dbg.dassert(chunk_size <= MAX_CHUNK_SIZE, f"Chunk size should be <= {MAX_CHUNK_SIZE}")
    # Create an s3 object to query.
    s3 = boto3.client("s3")
    # Query until the response is not truncated.

    continuation_token = None
    is_truncated = True
    while is_truncated:
        continuation_arg: Dict[str, Any] = {}
        if continuation_token is not None:
            continuation_arg["ContinuationToken"] = continuation_token
        s3_objects = s3.list_objects_v2(
            Bucket=s3_bucket,
            Prefix=key_prefix,
            MaxKeys=chunk_size,
            **continuation_arg
        )
        # Extract the `Key` from each element.
        keys = [content["Key"] for content in s3_objects["Contents"]]
        continuation_token = s3_objects.get("NextContinuationToken")
        is_truncated = s3_objects["IsTruncated"]
        yield keys


def get_last_modified(bucket: str, key: str) -> datetime.datetime:
    """
    Get last modified date of a file on S3.

    :param bucket: S3 bucket name. eg. `default00-bucket`
    :param key: the path to file eg. `kibot/some_file.csv`
    :return: last modified date of the file
    """
    is_valid_key(key, raise_=True)
    s3 = boto3.client("s3")
    response = s3.head_object(Bucket=bucket, Key=key)
    date_time: datetime.datetime = response["LastModified"].replace(tzinfo=None)
    return date_time


# #########################################
# Save load
# #########################################
def load_object(bucket: str, key: str, as_obj: bool = False, **kwargs: Any) -> Any:
    """
    Load file from the s3 storage.

    :param key: full file path without leading `/` or `s3://`
    :param bucket: bucket name
    :param as_obj: Return response body object as is.
                   Usually you may need this for .read() interface compatibility.
        Example:
        > file_obj = load_object(bucket, key, as_obj=True)
        > some_data = json.load(file_obj)
    :return: the loaded file
    """
    _LOG.info("Reading file '%s' from '%s' bucket", key, bucket)
    is_valid_key(key, raise_=True)
    # Check that file exists before loading.
    is_key_exists(bucket, key, raise_=True)
    # Get the object from s3 as bytes.
    s3_client = boto3.client("s3")
    response = s3_client.get_object(Bucket=bucket, Key=key)
    response_body = response.get("Body")
    if as_obj:
        _LOG.debug("Return file as object.")
        return response_body
    obj_bytes = response_body.read()
    # Load file.
    if "encoding" in kwargs:
        encoding = kwargs.get("encoding")
    else:
        encoding = "utf8"
    if key.endswith(".json"):
        # Load json file.
        try:
            obj = pd.read_json(io.BytesIO(obj_bytes), encoding=encoding, **kwargs)
        except ValueError:
            # For pd.Series saved as .json.
            obj = pd.read_json(
                io.BytesIO(obj_bytes), encoding=encoding, typ="series", **kwargs
            )
    elif key.endswith(".pkl"):
        # Load pickle file.
        obj = pickle.loads(obj_bytes, **kwargs)
    elif key.endswith(".csv.gz") or key.endswith(".csv"):
        if key.endswith(".csv.gz"):
            # Specify the gzip compression.
            kwargs.update({"compression": "gzip"})
        # Load csv file.
        obj = pd.read_csv(io.BytesIO(obj_bytes), encoding=encoding, **kwargs)
    elif key.endswith(".pq"):
        obj = pd.read_parquet(io.BytesIO(obj_bytes), **kwargs)
    else:
        raise ValueError(f"Unsupported filename extension in '{key}'")
    return obj


def save_object(obj: Any, bucket: str, key: str, **kwargs: Any) -> None:
    """
    Save object to the s3 storage with provided key.

    :param obj: a file to save
    :param bucket: bucket name
    :param key: full file path without leading `/` or `s3://`
    :return:
    """
    _LOG.info("Saving file '%s' to '%s' bucket", key, bucket)
    is_valid_key(key, raise_=True)
    s3_client = boto3.client("s3")
    if key.endswith(".json"):
        # Get JSON file as bytes object.
        json_buffer = io.BytesIO()
        obj.to_json(json_buffer, date_format="iso", indent=4, **kwargs)
        body = json_buffer.getvalue()
    elif key.endswith(".pkl"):
        # Get pickle file as bytes object.
        body = pickle.dumps(obj, **kwargs)
    elif key.endswith(".csv.gz") or key.endswith(".csv"):
        if key.endswith(".csv.gz"):
            # Specify the gzip compression.
            kwargs.update({"compression": "gzip"})
        # Get csv file as bytes object.
        csv_buffer = io.BytesIO()
        obj.to_csv(csv_buffer, index=False, **kwargs)
        body = csv_buffer.getvalue()
    else:
        raise ValueError(f"Unsupported filename extension in '{key}'")
    # Get the file path.
    # Save file.
    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=body,
    )


def upload_file(bucket: str, key: str, file_path: str) -> None:
    """
    Upload file to s3.

    :param bucket: bucket to copy a file in
    :param key: path to the file on s3
    :param file_path: path to the file to copy
    :return:
    """
    is_valid_key(key, raise_=True)
    # Check that file exists before uploading.
    p1_dbg.dassert_exists(file_path)
    # Init the s3 client.
    s3_client = boto3.client("s3")
    # Upload file to s3.
    _LOG.info(
        "Uploading local file '%s' to '%s' bucket, key='%s'",
        file_path,
        bucket,
        key,
    )
    s3_client.upload_file(
        Filename=file_path,
        Bucket=bucket,
        Key=key,
    )


def download_object(bucket: str, key: str, file_path: str) -> None:
    """
    Download object from s3 and save with provided file_path.

    :param bucket: the bucket to copy a file from
    :param key: path to the file on s3
    :param file_path: path to the copy
    :return:
    """
    is_valid_key(key, raise_=True)
    # Check that file exists before downloading.
    is_key_exists(bucket, key, raise_=True)
    # Create destination dirs and subdirs if they do not exist.
    hio.create_dir(os.path.dirname(file_path), incremental=True)
    # Init the s3 client.
    s3_client = boto3.client("s3")
    # Download file from s3.
    _LOG.info(
        "Downloading file '%s' from '%s` bucket in '%s'",
        key,
        bucket,
        file_path,
    )
    s3_client.download_file(
        Filename=file_path,
        Bucket=bucket,
        Key=key,
    )


def download_dir(bucket: str,
                 key_prefix: str,
                 dst_dir: str,
                 overwrite: bool = True,
                 exists_raise: bool = True) -> None:
    """
    Recursively download the folder.
    The folder is all objects with given key_prefix

    Note: there is no "dir" in s3, it's rather prefix for s3 key.

    :param bucket: bucket that contains the dir to copy
    :param key_prefix: dir to download files from
    :param dst_dir: dir to download files to
    :param overwrite: True - overwrite local files, False - do not overwrite local files
    :param exists_raise: True - raise exception if local file already exists
    :return:
    """
    _LOG.info("Downloading directory from s3. "
              f"bucket={bucket}, "
              f"key_prefix={key_prefix}, "
              f"dst_dir={dst_dir}, "
              f"overwrite={overwrite}, "
              f"exists_raise={exists_raise}")
    is_valid_key(key_prefix, raise_=True)
    is_prefix_exists(bucket, key_prefix)
    # Init the s3 client.
    s3_client = boto3.client("s3")
    # Get a list of all objects in the "dir".
    objects = s3_client.list_objects(Bucket=bucket, Prefix=key_prefix)
    obj = None
    try:
        for obj in objects["Contents"]:
            key = obj["Key"]
            # Check that file_path is not a dir name.
            if not key.endswith("/"):
                # Get the file relative path.
                file_rel_path = os.path.relpath(key, key_prefix)
                # Get the path to download the file to.
                dst_path = os.path.join(dst_dir, file_rel_path)

                if os.path.exists(dst_path):
                    _LOG.warning("File %s already exists." % dst_path)
                    if exists_raise:
                        raise FileExistsError("File exists exception. "
                                              "overwrite=%s, exists_raise=%s" % (
                                                  overwrite, exists_raise))
                    if overwrite:
                        _LOG.warning("Overwriting file %s." % dst_path)
                    else:
                        continue

                # Download files from s3 to the specified dir.
                download_object(
                    bucket=bucket,
                    key=key,
                    file_path=dst_path,
                )
    except Exception as e:
        _LOG.error(
            "Can't download '%s' directory from %s bucket. obj=%s" % (key_prefix, bucket, obj))
        raise e
