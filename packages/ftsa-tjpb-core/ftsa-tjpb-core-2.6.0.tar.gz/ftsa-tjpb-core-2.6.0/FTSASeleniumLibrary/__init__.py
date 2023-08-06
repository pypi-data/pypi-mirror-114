import logging

from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.keywords import BrowserManagementKeywords, ScreenshotKeywords, WaitingKeywords, \
                                     FormElementKeywords, ElementKeywords, JavaScriptKeywords
from robot.api import logger
from robot.api.deco import library, keyword

from shutil import which
import docker
import os
import socket
import time
from datetime import datetime

from ftsa.core.properties import VERSION, REMOTE_VERSION, SLEEP_SECONDS, REC_VIDEO_VERSION
from ftsa.core.utils import extract_name_from, extract_type_from, sanitize_camel_case, get_project_properties


@library(scope='GLOBAL', version=VERSION)
class FTSASeleniumLibrary(SeleniumLibrary):

    def __init__(self):
        SeleniumLibrary.__init__(self)

    @keyword
    def open_browser(self, url=get_project_properties().get('prop', 'URL'),
                     browser=get_project_properties().get('prop', 'BROWSER'), remote_url=None,
                     maximized=True, speed=get_project_properties().get('prop', 'SPEED'),
                     timeout=get_project_properties().get('prop', 'TIMEOUT'),
                     implicit_wait=get_project_properties().get('prop', 'IMPLICIT_WAIT'),
                     idiom=get_project_properties().get("prop", "IDIOM"),
                     download_path=f"output{os.sep}downloads"):
        """*FTSA opens a new browser instance*

        Open the ``browser`` with initial tests ``url``.

        Default options used:
        | browser       | chrome |
        | remote_url    | None   |
        | maximized     | True   |
        | speed         | 0.3s   |
        | timeout       | 20s    |
        | implicit_wait | 10s    |
        | idiom         | en-US  |
        | download_path | output/downloads (Chrome, only) |

        _Returns_ the *page title*

        """
        # Configuring DOWNLOAD_PATH
        download_path = os.path.join(os.getcwd(), download_path)
        if not os.path.isdir(download_path):
            os.mkdir(download_path)
            logger.info(f'Download directory created: "{download_path}"')
        else:
            logger.info(f'Directory already exists: "{download_path}"')

        # Configuring BROWSER OPTIONS
        browser_management = BrowserManagementKeywords(self)
        if browser.lower() == 'firefox':
            from selenium.webdriver.firefox.options import Options, FirefoxProfile
            config_options = Options()
            profile = FirefoxProfile(FirefoxProfile.DEFAULT_PREFERENCES)
            profile.set_preference("browser.download.folderList", 2)
            profile.set_preference("browser.download.manager.showWhenStarting", False)
            profile.set_preference("browser.download.dir", download_path)
            profile.set_preference("browser.helperApps.alwaysAsk.force", False)
            profile.set_preference("intl.accept_languages", idiom)
            profile.update_preferences()
            config_options.profile = profile
            config_options.binary = which("firefox")
            logger.info(f'Browser FIREFOX config options enabled.')
        elif browser.lower() == 'opera':
            from selenium.webdriver.opera.options import Options
            config_options = Options()
            config_options.binary = which("opera")
            logger.info(f'Browser OPERA config options enabled.')
        elif browser.lower() == 'edge':
            from selenium.webdriver.edge.options import Options
            config_options = Options()
            config_options.binary = which("edge")
            logger.info(f'Browser EDGE config options enabled.')
        elif browser.lower() == 'chrome':
            from selenium.webdriver.chrome.options import Options
            config_options = Options()
            logger.info(f'## Configuring Chrome Browser with download path created at "{download_path}" ##')
            config_options.add_experimental_option("prefs", {"download.default_directory": f"{download_path}",
                                                             "download.prompt_for_download": False,
                                                             "download.directory_upgrade": True,
                                                             "safebrowsing.enabled": True})
            config_options.add_argument(f'--lang={idiom}')
            config_options.binary = which("chrome")
            logger.info(f'Browser CHROME config options enabled.')
        else:
            raise RuntimeError(f'{browser} browser is not supported.')

        # Configuring MAXIMIZED
        if maximized:
            logger.info(f'Setting {browser.upper()} browser to open MAXIMIZED.')
            config_options.add_argument('--start-maximized')
        logger.info(f'Setting SELENIUM SPEED to "{speed}".')
        browser_management.set_selenium_speed(speed)
        logger.info(f'Setting SELENIUM TIMEOUT to "{timeout}".')
        browser_management.set_selenium_timeout(timeout)
        logger.info(f'Setting SELENIUM IMPLICIT WAIT to "{implicit_wait}".')
        browser_management.set_selenium_implicit_wait(implicit_wait)
        # Open Browsing with/without remote URL
        if remote_url is not None and os.getenv('NO_DOCKER_EXECUTION') != 'nodocker':
            browser_management.open_browser(url, browser, options=config_options, remote_url=remote_url)
            logger.info(f'Browser {browser.upper()} opened in remote url {remote_url}.')
        else:
            browser_management.open_browser(url, browser, options=config_options)
            logger.info(f'Browser {browser.upper()} opened locally.')
        return browser_management.get_title()

    @keyword
    def close_all_browsers(self):
        """*FTSA closes all open browsers*

        Closes all open browsers and resets the browser cache.

        """
        browser_management = BrowserManagementKeywords(self)
        screenshot = ScreenshotKeywords(self)
        screenshot.capture_page_screenshot()
        browser_management.close_all_browsers()

    @keyword
    def login_user(self, username, password, url=get_project_properties().get('prop', 'URL'), cas2=True):
        """*FTSA Login the user*

        FTSA Login the user with ``username`` and ``password`` into CAS2, before redirecting to the ``url``.

        | *Obs:* | To properly work, page must contains id locators to ``id:username`` and ``id:password``; and a submit button with ``name:submit`` locator |

        """
        logger.info(f'FTSA logins the "{username}" user with password "{password}" and, if cas2=True, redirects to "{url}"')
        browser_management = BrowserManagementKeywords(self)
        form_elements = FormElementKeywords(self)
        elements = ElementKeywords(self)
        waiting = WaitingKeywords(self)
        project = get_project_properties()

        cas_url = project.get('prop', 'CAS_URL')
        if cas2:
            # Go to CAS and Login
            logger.info(f'CAS2 Detected. Going to "{cas_url}"')
            browser_management.go_to(cas_url)

            # Click Login Again button
            login_again_button = "xpath://div[@id='content']//a[@href='/cas2/login']"
            waiting.wait_until_element_is_visible(locator=login_again_button)
            elements.click_element(locator=login_again_button)
        elif get_project_properties().get('prop', 'URL') != url:
            # Go to keyword specified URL
            logger.info(f'Going to keyword specified URL "{url}"')
            browser_management.go_to(url)

        # Set Username, Password and Submit
        waiting.wait_until_element_is_visible(locator='id:username')
        waiting.wait_until_element_is_visible(locator='id:password')
        form_elements.input_text(locator='id:username', text=username, clear=True)
        form_elements.input_text(locator='id:password', text=password, clear=True)

        elements.click_element("xpath://*[@type='submit']")

        # Wait 3 seconds and go to system URL
        time.sleep(3)
        if cas2 and url != cas_url:
            logger.info(f'CAS2 Detected and "{url}" is not equals to "{cas_url}. Going to "{url}"')
            browser_management.go_to(url)

    @keyword
    def input_text_js(self, locator, value):
        """*FTSA input text directly from javascript*

        FTSA Input Text JavaScript with ``locator`` and ``value``. You must declare into ``locator`` type and name like this: "id:username", "xpath://input[0]", etc.

        Available ``locator`` types are: id, className, name, tagName, cssSelector and xPath

        Examples of use:
        | INPUT TEXT JS | id:username | john |
        | INPUT TEXT JS | name:password | john123 |

        *Obs:* for locator types different from ``id``, click only applied to the first result encountered.

        """
        the_type = extract_type_from(locator)
        name = extract_name_from(locator)
        javascript = JavaScriptKeywords(self)
        waiting = WaitingKeywords(self)
        waiting.wait_until_element_is_visible(locator=locator)

        if the_type.lower() == 'id':
            javascript.execute_javascript(f'document.getElementById("{name}").value = "{value}";')
        elif the_type.lower() == 'classname':
            javascript.execute_javascript(f'document.getElementsByClassName("{name}")[0].value = "{value}";')
        elif the_type.lower() == 'name':
            javascript.execute_javascript(f'document.getElementsByName("{name}")[0].value = "{value}";')
        elif the_type.lower() == 'tagname':
            javascript.execute_javascript(f'document.getElementsByTagName("{name}")[0].value = "{value}";')
        elif the_type.lower() == 'cssselector':
            javascript.execute_javascript(f'document.querySelectorAll("{name}")[0].value = "{value}";')
        elif the_type.lower() == 'xpath':
            javascript.execute_javascript(
                f'document.evaluate("{name}", document, null, '
                f'XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.value = "{value}";')
        else:
            raise Exception(f'"{the_type}" is not a valid locator type!')

    @keyword
    def click_element_js(self, locator):
        """*FTSA input text directly from javascript*

        FTSA Input Text JavaScript with ``locator`` and ``value``. You must declare into ``locator`` type and name like this: "id:confirm", "xpath://button[0]", etc.

        Available ``locator`` types are: id, className, name, tagName, cssSelector and xPath

        Examples of use:
        | CLICK ELEMENT JS | id:confirm |
        | CLICK ELEMENT JS | name:submit |

        *Obs:* for locator types different from ``id``, click only applied to the first result encountered.

        """
        the_type = extract_type_from(locator)
        name = extract_name_from(locator)
        logger.info(f'\n\nSearching for element TYPE = {the_type} ; and LOCATOR NAME = {name}\n\n')
        javascript = JavaScriptKeywords(self)
        waiting = WaitingKeywords(self)
        waiting.wait_until_element_is_visible(locator=locator)

        if the_type.lower() == 'id':
            javascript.execute_javascript(f'document.getElementById("{name}").click();')
        elif the_type.lower() == 'classname':
            javascript.execute_javascript(f'document.getElementsByClassName("{name}")[0].click();')
        elif the_type.lower() == 'name':
            javascript.execute_javascript(f'document.getElementsByName("{name}")[0].click();')
        elif the_type.lower() == 'tagname':
            javascript.execute_javascript(f'document.getElementsByTagName("{name}")[0].click();')
        elif the_type.lower() == 'cssselector':
            javascript.execute_javascript(f'document.querySelectorAll("{name}")[0].click();')
        elif the_type.lower() == 'xpath':
            javascript.execute_javascript(
                f'document.evaluate("{name}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();')
        else:
            raise Exception(f'"{the_type}" is not a valid locator type!')

    @keyword
    def init_remote_server(self, browser=get_project_properties().get('prop', 'BROWSER'),
                           network_name="grid", selenium_name='selenium',
                           port="4444", ):
        """*FTSA initialize remote server*

        FTSA creates a new container instance to run FTSA-TJPB tests inside, with the following configurations:

        | browser | The name of the browser: chrome, firefox, opera or edge are allowed |
        | network_name | The name used to run/up network, by default: grid |
        | selenium_name | The name used to run/up selenium container, by default: selenium |
        | port | The external available port (entrypoint) to the container, by default: 4444 |

        ***If USER_GRID_NAME environment variable is set, it will be used to replace 'grid_name' during network setup.***
        ***If SELENIUM_NAME environment variable is set, it will be used to replace 'selenium_name' during container up.***
        ***If SELENIUM_EXEC_HOST environment variable is set, it will be used to replace the default hostname machine
        (you may use IP directly, for example).***
        """
        # Does execution allows docker?
        if os.getenv('NO_DOCKER_EXECUTION') == 'nodocker':
            logger.info('Keyword ignored. Docker is not allowed for this execution')
            return {
                "host": None,
                "port": None,
                "network_name": None,
                "selenium_name": None
            }
        else:
            docker_client = docker.from_env()
            if browser == "firefox":
                browser_image_name = f'selenium/standalone-firefox:{REMOTE_VERSION}'
            elif browser == "opera":
                browser_image_name = f'selenium/standalone-opera:{REMOTE_VERSION}'
            elif browser == "edge":
                browser_image_name = f'selenium/standalone-edge:{REMOTE_VERSION}'
            elif browser == "chrome" or browser == "chromium":
                browser_image_name = f'selenium/standalone-chrome:{REMOTE_VERSION}'
            else:
                raise RuntimeError(f'{browser} browser is not supported.')

            # Initializing NETWORK
            network_name_env = os.getenv('USER_NETWORK_NAME')
            if network_name_env is not None:
                network_name = network_name_env
            try:
                network = docker_client.networks.get(network_name)
            except BaseException:
                network = docker_client.networks.create(network_name)
            logger.info(f'{network.attrs}')
            logger.info(f'Network "{network_name}" initialized.')

            # Initializing SELENIUM container
            selenium_name_env = os.getenv('SELENIUM_CONTAINER_NAME')
            if selenium_name_env is not None:
                selenium_name = selenium_name_env
            try:
                selenium = docker_client.containers.get(selenium_name)
            except BaseException:
                selenium = docker_client.containers.run(
                    name=f'{selenium_name}', network=f'{network_name}',
                    image=f'{browser_image_name}',
                    detach=True, privileged=False,
                    ports={
                        f'{port}': '4444',
                        '6900': '5900'
                    }
                )
            selenium.logs()
            logger.info(f'{selenium.attrs}')
            logger.info(f'Selenium container "{selenium_name}" initialized into "{network_name}" network.')
            time.sleep(SLEEP_SECONDS)

            host = os.getenv('SELENIUM_EXEC_HOST')
            if host is None:
                host = socket.gethostbyname(socket.gethostname())
            logger.info(f'Server {host}:{port} initialized.')

            return {
                "host": host,
                "port": port,
                "network_name": network_name,
                "selenium_name": selenium_name
            }

    @keyword
    def end_remote_server(self, network_name="grid", selenium_name="selenium"):
        """*FTSA finalizes remote server*

        FTSA finalizes remote server:

        | network_name | The name used to run/up network, by default: grid |
        | selenium_name | The name used to run/up selenium container, by default: selenium |

        ***If USER_EXEC_CONTAINER environment variable is set, it will be used to finish the server.***
        """
        # Does execution allows docker?
        if os.getenv('NO_DOCKER_EXECUTION') == 'nodocker':
            logger.info('Keyword ignored. Docker is not allowed for this execution')
        else:
            docker_client = docker.from_env()

            # Stopping and removing Selenium container
            selenium_name_env = os.getenv('SELENIUM_CONTAINER_NAME')
            if selenium_name_env is not None:
                selenium_name = selenium_name_env
            try:
                selenium = docker_client.containers.get(selenium_name)
                selenium.stop()
                selenium.remove()
                logger.info(f'Selenium container "{selenium_name}" stopped and removed.')
            except BaseException:
                logger.info(f'There is no {selenium_name} container available.')
            time.sleep(SLEEP_SECONDS)

            # Removing NETWORK
            network_name_env = os.getenv('USER_NETWORK_NAME')
            if network_name_env is not None:
                network_name = network_name_env
            try:
                network = docker_client.networks.get(network_name)
                network.remove()
                logger.info(f'Network "{network_name}" removed.')
            except BaseException:
                logger.info(f'There is no {network_name} network available.')

    @keyword
    def init_record_test_video(self, test_name=None, video_name="video", network_name="grid",
                               selenium_name="selenium"):
        """*FTSA initialize record test video*

        FTSA creates a new container instance to record test video, with the following configurations:

        | test_name | Inform the test case name. By defult, None. |
        | network_name | The name used to initialize network, by default: grid |
        | video_name | The name user to run/up video recording container, by default: video |
        | selenium_name | The name user to reference selenium browser container, by default: selenium |
        """
        # Does execution allows docker?
        if os.getenv('NO_DOCKER_EXECUTION') == 'nodocker':
            logger.info('Keyword ignored. Docker is not allowed for this execution')
        else:
            docker_client = docker.from_env()

            # Creating videos directory AND...
            videos_path = f'{os.getcwd()}{os.sep}videos'
            if not os.path.isdir(videos_path):
                os.makedirs(videos_path)
            # ... Setting volume video recording name
            if os.getenv('VOLUME_VIDEO_RECORDING_NAME') is not None:
                videos_path = 'video_recording_volume'
            logger.info(f'Videos Path or Recording value enable to store recordings: "{videos_path}".')

            # Sanitizing Test name
            if test_name is not None:
                test_name = f'-{sanitize_camel_case(test_name)}'
            logger.info(f'Test Name value sanitized: "{test_name}".')

            # Getting Selenium Container name
            selenium_name_env = os.getenv('SELENIUM_CONTAINER_NAME')
            if selenium_name_env is not None:
                selenium_name = selenium_name_env
            logger.info(f'Selenium Container name: "{selenium_name}".')

            # Getting Network name
            network_name_env = os.getenv('USER_NETWORK_NAME')
            if network_name_env is not None:
                network_name = network_name_env
            logger.info(f'Network name: "{network_name}".')

            # Initializing Videos Recorder Container
            video_image_name = f'selenium/video:{REC_VIDEO_VERSION}'
            video_name_env = os.getenv('VIDEOS_RECORDER_CONTAINER_NAME')
            if video_name_env is not None:
                video_name = video_name_env
            try:
                video = docker_client.containers.get(video_name)
            except BaseException:
                now = datetime.now().strftime("%Y%m%d%H%M%S")
                video = docker_client.containers.run(
                    name=f'{video_name}', network=f'{network_name}',
                    image=f'{video_image_name}',
                    detach=True, privileged=False,
                    environment=[
                        f'DISPLAY_CONTAINER_NAME={selenium_name}',
                        f'FILE_NAME={now}{test_name}-video.mp4'
                    ],
                    volumes={
                        f'{videos_path}': {'bind': '/videos', 'mode': 'rw'}
                    }
                )
            video.logs()
            logger.info(f'{video.attrs}')
            logger.info(f'Videos recorder container "{video_name}" initialized into "{network_name}" network.')
            time.sleep(SLEEP_SECONDS)

    @keyword
    def end_record_test_video(self, video_name="video"):
        """*FTSA finalizes record test video*

        FTSA finalizes remote test video recorder:

        | video_name | The name used to run/up video container, by default: video |
        """
        # Does execution allows docker?
        if os.getenv('NO_DOCKER_EXECUTION') == 'nodocker':
            logger.info('Keyword ignored. Docker is not allowed for this execution')
        else:
            docker_client = docker.from_env()
            video_name_env = os.getenv('VIDEOS_RECORDER_CONTAINER_NAME')
            if video_name_env is not None:
                video_name = video_name_env
            try:
                video = docker_client.containers.get(video_name)
                video.stop()
                video.remove()
                logger.info(f'Video container "{video_name}" was stopped and removed.')
            except BaseException:
                logger.info(f'There is no "{video_name}" container available.')
            time.sleep(2 * SLEEP_SECONDS)
