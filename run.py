from logger import logger
from downloader import ImageDownloader, DownloaderException, InvalidFormatException

TEXT_FILE_PATH = 'sample.txt'
DOWNLOAD_DIRECTORY = ''


def main(file_path, download_path):
    """
    Opens the text file and initiate image download.
    :param file_path: Path to the text file containing image urls
    :param download_path: The path to the download directory
    """
    try:
        with open(file_path, 'r') as fp:
            logger.info('Opening text file from {}'.format(file_path))
            for line in fp:
                url = line.rstrip('\n')
                try:
                    file_path = ImageDownloader().download_and_save_file(url, download_path)
                    logger.info('Image downloaded successfully. URL: {}. File path: {}'.format(url, file_path))
                except InvalidFormatException:
                    logger.exception('The downloaded file from URL: {} is not an image'.format(url))
                except DownloaderException as e:
                    logger.exception(str(e))
    except Exception as e:
        logger.exception('Error while opening text file. Error : {}'.format(str(e)))
    logger.info('Image download complete!')


if __name__ == '__main__':
    main(TEXT_FILE_PATH, DOWNLOAD_DIRECTORY)
