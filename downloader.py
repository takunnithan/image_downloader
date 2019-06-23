import requests
import os
import cgi
import uuid
import shutil


class BaseDownloader:

    def is_downloaded_file_valid(self, response):
        """
        Check for various file validations here. Returns a Boolean based on the validation result.
        This method is meant to be overridden by the subtypes of BaseDownloader
        :param response: Response object from requests(lib)
        :return: Bool, True if the validation succeeds, False otherwise
        """
        return True

    def get_file_name(self, response_headers):
        """
        Return file name from Response object Or construct one
        :param response_headers: HTTP headers from Response object - requests(lib)
        :return: str: Name for the downloaded file
        """
        header = cgi.parse_header(response_headers.get('content-disposition', ''))[1]
        file_name = header.get('filename')
        if not file_name:
            file_type = response_headers.get('content-type', '').split('/')[-1]
            file_name = '{}.{}'.format(str(uuid.uuid4().hex), file_type)
        return file_name

    def download(self, file_url):
        """
        Downloads the file from the given URL.
        :param file_url: The URL of the file to be downloaded
        :return: Response: Response object with downloaded file
        """
        if not file_url:
            raise DownloaderException('Invalid file URL')
        res = requests.get(file_url, stream=True)
        if res.status_code == 200 and self.is_downloaded_file_valid(res):
            return res
        else:
            raise DownloaderException(
                'Failed to download the file. Error: {}'.format(str(self.construct_error_details(res))))

    def save_file(self, file_path, response):
        """
        Save the downloaded file to the specified path
        :param file_path: Directory path to save file
        :param response: Response object with downloaded file
        :return: str: Path to the saved file
        """
        file_name = self.get_file_name(response.headers)
        file_path = os.path.join(file_path, file_name)
        with open(file_path, 'wb') as fp:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, fp)
        return file_path

    def construct_error_details(self, response):
        """
        Construct meaningful error message for the download failure
        :param response: Response object from requests
        :return: str: Failure details
        """
        error_details = {
            'response': str(response.content),
            'status_code': response.status_code,
            'request_headers': response.request.headers,
            'response_headers': response.headers
        }
        return error_details


class ImageDownloader(BaseDownloader):
    """Downloads Image files"""

    image_formats = ['bmp', 'gif', 'jpeg', 'jpg', 'svg', 'tiff', 'ico', 'rgb', 'png', 'webp']

    def is_downloaded_file_valid(self, response):
        file_type = response.headers.get('content-type', '').split('/')[0]
        if file_type.lower() == 'image':
            return True
        else:
            header = cgi.parse_header(response.headers.get('content-disposition', ''))[1]
            file_extension = header.get('filename', '').split('.')[-1]
            if file_extension.lower() in self.image_formats:
                return True
        raise InvalidFormatException('Downloaded file is not an Image')

    def download_and_save_file(self, image_url, download_path):
        response = self.download(image_url)
        return self.save_file(download_path, response)


class DownloaderException(Exception):
    pass


class InvalidFormatException(Exception):
    pass
