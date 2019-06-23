from unittest.mock import patch, Mock, mock_open

import pytest
import builtins

from downloader import BaseDownloader, ImageDownloader, DownloaderException, InvalidFormatException


#    BaseDownloader

@patch('downloader.requests.get')
def test_download(mock_obj):
    mock_obj.return_value.status_code = 200

    response = BaseDownloader().download('test_url')
    assert response.status_code == 200, 'Wrong status code'

    mock_obj.return_value.status_code = 400
    with pytest.raises(DownloaderException):
        BaseDownloader().download('test_url')

    with pytest.raises(DownloaderException):
        BaseDownloader().download(None)


def test_get_file_name():
    response_headers = {'content-disposition': 'attachment; filename="test.png"; filename*=UTF-8\\test.png'}

    file_name = BaseDownloader().get_file_name(response_headers)
    assert file_name == 'test.png', 'Wrong file name'


def test_get_file_name_with_no_content_disposition_header():
    response_headers = {'content-type': 'image/jpg'}

    file_name = BaseDownloader().get_file_name(response_headers)
    assert 'jpg' in file_name, 'Wrong file name'


def test_construct_error_details():
    response = Mock()
    response.content = '<html>Invalid URL </html>'
    response.status_code = 400
    response.request.headers = {'test_header': 'header_value'}
    response.headers = {'content-type': 'text/html'}

    error_details = BaseDownloader().construct_error_details(response)

    assert error_details.get('status_code') == 400, 'Wrong status code'


@patch('downloader.shutil.copyfileobj')
def test_save_file(mock_obj):
    response = Mock()
    response.headers = {'content-disposition': 'attachment; filename="test.png"; filename*=UTF-8\\test.png'}
    file_path = '/test/images'

    open_ = mock_open()
    with patch.object(builtins, "open", open_):
        response = BaseDownloader().save_file(file_path, response)
    assert '/test/images/test.png' == response, 'Wrong file path'


# ImageDownloader


def test_is_downloaded_file_valid_with_valid_scenario():
    response = Mock()
    response.headers = {'content-type': 'image/jpg'}

    is_valid = ImageDownloader().is_downloaded_file_valid(response)

    assert is_valid, 'Not an Image file'


def test_is_downloaded_file_valid_with_no_content_disposition_header():
    response = Mock()
    response.headers = {'content-type': 'application/json'}
    with pytest.raises(InvalidFormatException):
        ImageDownloader().is_downloaded_file_valid(response)


def test_is_downloaded_file_valid_with_content_disposition_header():
    response = Mock()
    response.headers = {'content-disposition': 'attachment; filename="test.png"; filename*=UTF-8\\test.png'}
    is_valid = ImageDownloader().is_downloaded_file_valid(response)
    assert is_valid, 'Not an Image file'


def test_is_downloaded_file_valid_with_wrong_file_type():
    response = Mock()
    response.headers = {'content-disposition': 'attachment; filename="test.pdf"; filename*=UTF-8\\test.pdf'}
    with pytest.raises(InvalidFormatException):
        ImageDownloader().is_downloaded_file_valid(response)
