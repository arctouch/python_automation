# Python Automation

Python Automation is a generic multiplatform test automation structure.

Features:
* Parallel testing;
* Cross-browser testing;
* Cross-platform testing;
* Mobile Native and Web Application testing;
* Open Source;
* Free;
* Mock server;
* Low Level of Maintenance.

The framework consists in:

* [Behave](https://github.com/behave/behave): Cucumber implementation in python;
* [Selenium](https://selenium-python.readthedocs.io/): Run Automation for web applications;
* [Appium](http://appium.io/docs/en/about-appium/api/): Run Automation for web/mobile native applications.

# Table of Contents

<!--ts-->
* [Python Automation](#python-automation)
* [Table of Contents](#table-of-contents)
* [Installation](#installation)
    * [Environment Setup](#environment-setup)
    * [Automatic Installation](#automatic-installation)
    * [Quickstart Installation](#quickstart-installation)
    * [Detailed Installation](#detailed-installation)
* [Tech Details](#tech-details)
    * [Pages](#pages)
    * [Locators](#locators)
    * [Run Automation Locally](#run-automation-locally)
    * [Run Automation on SauceLabs](#run-automation-on-saucelabs)
    * [Continuous Integration](#continuous-integration)
        * [Jenkins Integration Example](#jenkins-integration-example)
    * [Mock Server](#mock-server)
* [Get Started](#get-started)
    * [Configuring the Project](#configuring-the-project)
        * [Mobile Native Application](#mobile-native-application)
        * [Web Application](#web-application)
    * [Creating a new Step](#creating-a-new-step)
    * [Creating a new Page](#creating-a-new-page)
* [Appendix](#appendix)
    * [Element Inspection](#element-inspection)
    * [SauceLabs Build Uploader](#saucelabs-build-uploader)
<!--te-->

# Installation

* [Environment Setup](#environment-setup)

* [Manually](#manually)

## Environment Setup

In order to use simulators you will need to have the following IDEs installed

### Xcode

If you do not have it installed, you can download it from AppStore or [developer.apple.com](https://developer.apple.com)

### Android Studio

If you do not have it installed, you can download it from [developer.android.com](https://developer.android.com/studio)

Don't forget to add the ANDROID_HOME environment variable:

For bash:

```$ nano ~/.bash_profile```

For zsh:

```$ nano ~/.zshenv```

Then add:

```export ANDROID_HOME="/Users/{USERNAME}/Library/Android/sdk"```
```export PATH=$ANDROID_HOME/platform-tools:$PATH```

Finally, run:

```$ source ~/.bash_profile``` or ```$ source ~/.zshenv```

### Java JDK 8

If you do not have it installed, you can download it from [oracle.com](https://www.oracle.com/java/technologies/downloads/#jdk19-mac)

Don't forget to add the JAVA_HOME environment variable:

For bash:

```$ nano ~/.bash_profile```

For zsh:

```$ nano ~/.zshenv```

Then add the following lines:

```export JAVA_HOME="/Library/Java/JavaVirtualMachines/{PACKAGE}/Contents/Home"```

```export PATH=$JAVA_HOME/bin:$PATH```

Finally, run:

```$ source ~/.bash_profile``` or ```$ source ~/.zshenv```

## Automatic Installation
Run:

```$ sh install.sh```

## Quickstart Installation

Install Python 3 (MacOS brings Python 2 as system default):

```$ brew install python3```

Edit bash_profile file to execute everything with the newest Python version:

for bash:

```$ nano ~/.bash_profile```

for zsh:

```$ nano ~/.zshenv```

Add the following line (kill the terminal to save the bash changes):

```alias python=python3```

PIP installation (needs Python 3):

```$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py```

```$ python get-pip.py```

Open core_files folder:

```$ cd python-automation/core_files```

Install virtualenv package:

```$ pip install virtualenv```

Create virtual environment inside core_files folder:

```$ virtualenv automation_virtualenv```

Activate the virtual environment:

```$ source automation_virtualenv/bin/activate```

Install project dependencies (from core_files folder):

```$ pip install -r requirements.txt```

Install node to then install Appium:

```$ brew install node```

Install Appium:

```$ npm install -g appium```

Install appium-doctor, to install Appium dependecies:

```$ npm install -g appium-doctor```

Then run:

```$ appium-doctor```

After all Appium dependecies properly set up, you should be ready to go to [Run Automation](#run-automation) section.

## Detailed Installation
### Python Setup

First, you'll need Python 3 to use this project. You can get it easily with brew:

```$ brew install python3```

Depending on your environment, the symlinks ```brew``` creates can be different. It's commonly `python` or `python3`. To know which one is the correct one, just run these commands followed by ```--version```, and check if the version is > 3.6. Then just use the one that has a 3.x as your default one.

```$ python --version```

```$ python3 --version```

> :warning: In case your version is 2.7, that's the default MacOS version, and it WON'T RUN the automation. In this case, try going to the [python official download page](https://www.python.org/downloads/) and follow the tutorial there.

#### pip

Just follow the instructions on this link https://pip.pypa.io/en/stable/installing/

### Dependencies Setup

#### Setup virtual environment
If you don't have virtualenv installed in your machine, run the following command:

```$ pip install virtualenv```

This will make sure the dependencies are installed at the project level and prevent issues with system wide installations.

```$ virtualenv automation_virtualenv```

Before installing dependencies, we need to activate the `virtualenv` by running:

```$ source automation_virtualenv/bin/activate```

#### Requirements

To install the dependencies, just run:

```$ pip install -r requirements.txt```

If you created a virtualenv, it will install only on it. Otherwise, it will install in your system. In some cases, the installation may fail, recomending you to run with `--user`. Just run `$ pip install --user -r requirements.txt`.

#### Create Device Config File

On terminal (from `core_files` folder), just run:

```$ python support/generator/generate_devices_config.py```

This command will update the file ```resources/device_config.json```, that contains all information needed for the device capabilities.

**Note:** for now this command only updates the capabilities for iOS device simulators.

### Appium Setup

To install the Appium server, you'll need ```npm```, which comes with the ```node``` brew package:

```$ brew install node```

After that run:

```$ npm install -g appium```

#### Appium Doctor

Appium also needs some dependencies to work. I won't cover all of them (since there are a lot of dependencies), but to see if you have any environments issues, you just need to run ```appium-doctor```, which you can get with:

```$ npm install -g appium-doctor```

# Tech Details

## Pages

Every page object **must have** the following pre-requisites:

- Must inherit the [`BasePage`](core_files/support/pages/base.py) class before any other class.
- Must inherit the [element classes](core_files/support/elements/) that the page is gonna use, otherwise it won't have valid methods to execute on the steps.
- Should call `super().__init__(context)` on it's constructor.
- Should define a `locator` object on it's constructor, and it should have valid locator dictionaries.
- Should have a `navigate()` method defined, which will execute actions on other pages to reach your page.
- Should have a `page_is_displayed()` method defined, and the same should verify that a unique element is appearing on the screen.

## Locators

Locators should always have a dictionary of locators for each element you're testing. Element is the class that's responsible to handle it. The queries of this class should be the name
that will match the step call (these keys are the parameters), and the value should be `'ios'`, `'android'` and `'web'` as locators.

In `By.SOMETHING`, the `By` stands as an abreviation of `MobileBy`, which is a function imported from `appium.webdriver.common.mobileby`. While `SOMETHING` stands for the way or tool it will use to locate the given string.

The `Element Name` is the name that will be used to refer to this element when writing test scenarios. When the program reads `Element Name` in the scenario, it will understand that it's trying to search for an element with `name='Element Name'`.

The `Element.type`, as the name suggests, is the kind of that element. So for example it might be an `image`, `label`, `button`, `section` and so on.

Example:

```python
ELEMENT_NAME = Element.type(
    name='Element Name',
    ios_query=(By.ACCESSIBILITY_ID, 'Matches'),
    android_query=(By.ANDROID_UIAUTOMATOR, get_text('Matches')),
    web_query=(By.ID, 'Matches')
)
```

## Run Automation Locally
All devices' names should be configured on: [device_config.json](core_files/resources/device_config.json).

[Python Virtual Environment](#setup-virtual-env) is mandatory to run the code, don't miss this configuration.

### Run the automation code
Firstly, make sure you're on `core_files` folder. Then run:

`$ python runner.py --d name1,name2`

If you want to run Web Automation:

`$ python runner.py --d name1,name2 --web`

### Tagging expression
If you want run the automation of a specific tag, then run:

`$ python runner.py --d name1,name2 --tag automation,ios`

## Run Automation on SauceLabs
Firstly, make sure that your SauceLabs credentials (username and accessKey) are properly set on [app_config.yaml](core_files/resources/app_config.yaml)

```
Appium:
  port: 4273
  systemPort: 8200
  username: sauce_labs_username
  accessKey: SAUCE-LABS-ACCESS-KEY
```

All devices' names should be configured on: [device_config.json](core_files/resources/device_config.json).

We have the setup for some mobile devices:

```
    {
      "name": "AnyiPhone11",
      "deviceName": "iPhone 11.*",
      "platformName": "ios",
      "automationName": "XCuiTest",
      "platformVersion": "14"
    },
```

and for some Desktop Browsers:

```
    {
      "name": "ChromeLinux",
      "platformName": "web",
      "platform": "Linux",
      "browserName": "chrome",
      "version": "latest"
    },
```

### Upload your application to SauceLabs File Storage
You need to upload your application on SauceLabs File Storage to run the tests on the proper build. The filename should match the filename used on [app_config.yaml](core_files/resources/app_config.yaml).

To upload, run:
```
curl -u "$SAUCE_USERNAME:$SAUCE_ACCESS_KEY" --location \
--request POST 'https://api.us-west-1.saucelabs.com/v1/storage/upload' \
--form 'payload=@"PATH/OF/YOUR/FILE.apk"' \
--form 'name="name_of__your_file.apk"' \
--form 'description="An awesome description"'
```

### Run the automation code
Firstly, make sure you're on `core_files` folder. Then run:

`$ python runner.py --d name1,name2 --saucelabs`

If you want to run Web Automation:

`$ python runner.py --d name1,name2 --web --saucelabs`

## Continuous Integration

This project is configured to provide JUnit reports in XML by default.

After execution, the reports are stored on [reports](core_files/reports). They are divided by the each feature file and by device name.

There is an example of how Jenkins presents the reports:

![JUnit Report](doc/images/JUnitReport.png)

### Jenkins Integration Example

In case of Mobile Native Application, the project can be a Jenkins job similar as the Application job. The Automation job need to be the down-stream job of the Application job. Also, the test automation project should have the latest build to test the application.

We should configure it via shell script saying that Jenkins will need to make a copy/paste to drag and drop the latest build into the [apps](core_files/resources/apps) folder.

There is an example of how Jenkins can handle the test automation solution inside the continuous delivery:

![Job cycle](doc/images/jenkins_execution.png)

It's essential to have the latest version of the develop branch on Jenkins server. So, every new build executed by the Application job will execute the Automation job, copy/paste the new Application build and then run the tests.

## Mock server
During the tests, there are some situations that we need to have some pre-defined data.

For example:
- Test how the app presents the X screen without Y section;
- Test how the app presents the Z tab without something happening;
- Changing the test user entitlements.

To solve this problem, we're using a mock server solution. This project uses the BaseHTTPRequestHandler library as proxy. Basically, this solution emulates a Mock Server at localhost. The endpoint that we want to mock will be configured inside [`endpoints.py`](core_files/support/constants/mocks/endpoints.py).

We can configure more than one BASE_URL and configure them separately.

To trigger the different endpoints, you should set the proper scenario tag and match it at [`environment.py`](core_files/features/environment.py).

This solution expects to have all mock data used by Mock Server inside [`mocks`](core_files/support/constants/mocks) folder. The name of the JSON file should be the same of the `API_ENDPOINT` environment variable.

By default, the Mock Server is configured to run on http://127.0.0.1:53209 but you can change this configuration at [`app_config.yaml`](core_files/resources/app_config.yaml).

### For mobile apps

To have success using the Mock Server on mobile apps, you should set the device's proxy configuration to use the computer IP. It should be easily done by configuring Charles Proxy. After that, the desired endpoint should be redirected (Map Remote) to http://127.0.0.1:53209. So the application will get the mock data.

# Get Started

## Configuring the project
>With the devices configured properly, we can run the test automation for native mobile applications with the Get Started example that's already configured on the project. Enjoy!

### Native Mobile Application
Firstly, you need to put the .apk and .ipa files in the [apps](core_files/resources/apps) folder.

Configure the application capabilities on [app_config.yaml](core_files/resources/app_config.yaml), you'll need to substitute all the information.

The [device_config.json](core_files/resources/device_config.json) file should be configured with the correct device information.

Check the following example for iOS and Android devices:

<details>
  <summary>Android</summary>

```json
    {
        "name": "personal-real",
        "deviceName": "0047503804",
        "platformName": "android",
        "udid": "0047503804",
        "automationName": "UIAutomator2",
        "platformVersion": "9"
    },
```
</details>

<details>
<summary>iOS</summary>

```json
    {
        "name": "PAP302-real",
        "deviceName": "PAP302",
        "platformName": "ios",
        "udid": "00008020-0011515C369A002E",
        "automationName": "XCUITest",
        "platformVersion": "12.0"
    },
```
</details>

### Web Application
Configure the URL of the Web Application on `address` property at the [app_config.yaml](core_files/resources/app_config.yaml) file and remove `app` property.

>`app` and `address` are both optional because they should not be added on the same platform. So, you'll need to replace these properties accordingly to the automation type.

The [device_config.json](core_files/resources/device_config.json) file should be configured with the correct device's information.

Check the following example for iOS, Android and Desktop devices:

<details>
  <summary>Android</summary>

```json
    {
        "name": "personal-real",
        "deviceName": "0047503804",
        "platformName": "android",
        "udid": "0047503804",
        "automationName": "UIAutomator2",
        "platformVersion": "9",
        "browserName": "Chrome"
    },
```
</details>

<details>
<summary>iOS</summary>

```json
    {
        "name": "PAP302-real",
        "deviceName": "PAP302",
        "platformName": "ios",
        "udid": "00008020-0011515C369A002E",
        "automationName": "XCUITest",
        "platformVersion": "12.0",
        "browserName": "Safari"
    },
```
</details>

<details>
<summary>Desktop</summary>

```json
    {
        "name": "chrome-mac",
        "platformName": "web",
        "browserName": "chrome",
        "version": "83.0"
    },
```
</details>

>Don't forget to run the code with `--web` flag (see [Run Automation](#run-automation)) in case of Web automation.

## Creating a new Step
Every new scenario that don't follow a pre-defined step must be implemented on [steps](core_files/features/steps) folder. Essentially, the files are divided by general steps and specific steps. Every new step that is really specific for a page need to be implemented on a specific step file.

For example:
```gherkin
    When the user types his credentials
```

This step is implemented in [login_steps.py](core_files/steps/login_steps.py):
```python
@when("the user types his credentials")
def type_credentials(context):
    page = LoginPage(context)
    assert page.is_current_page, f"{page} is not current page"
    page.type_credentials(context.user)
```

## Creating a new Page
There are some steps to follow for a new Page creation:

Firstly, we need to create the Page file on the [pages](/core_files/pages) folder. The page's structure need to follow a pattern (see [Pages](#pages) section), you can copy/paste an example of any other existing page.

The class name should follow the format: `PageNamePage` (considering that the name is: "Page Name").

The Elements should be created following the pattern described on [Locators](#locators) section. It's essential to create friendly internal identifiers to refer each element.

>Tip: the internal identifiers can be the same of the locator IDs, it will help to keep the automation with low level of maintenance.

With all Elements, we can configure the `trait` method to return the element that will be responsible to say that the page is displayed.

The `previous_screen` method should be configured returning the page that preceeds the current page.

```python
    @property
    def previous_screen(self):
        from pages import LoginPage
        return LoginPage(self.context)
```

The `path_switcher` method should be configured with the actions that the Application will perform to navigate to the next pages. It's essential to create a new method (i.e. `log_in_default_user`) to perform the action using the `BasePage` file. So, in this case, to access the `HomePage`, the application need to login in with valid credentials.

```python
    @property
    def path_switcher(self):
        from pages import HomePage

        paths = {
            HomePage: self.log_in_default_user
        }

        return paths
```

Check the following diagram to better understand how the pages work together:
![Pagination diagram](doc/images/diagram_pages.png)

To finish the page creation, we should configure the [__init__.py](/core_files/pages/__init__.py) file with the ClassName and the Filename of the new page.

# Appendix

## Element inspection
1. Using Appium UI inspector
    1. Installing Appium UI
            - Download and install [Appium UI](http://appium.io)
    1. Executing Appium UI:
        1. Open Appium UI
        1. Click on "Start Server" button
        1. On the top right corner, tap over the "Start Inspector Session" button
        1. On the Automatic Server tab, set the [desired capabilities](#desired-capabilities) for Android or iOS devices
        1. Click on "Start Session" button
        1. Inspect Elements:
            1. On the Appium Inspector window, you should be able to see the screen of the app
            1. Select any element on the screen to inspect their characteristics
            1. IMPORTANT: navigate on the app ONLY through the Appium Inspector. When needed to access another screen, click over the element on the Appium Inspector and, on the "Selected Element" window, use the "tap" command.
1. Accessibility Inspector (iOS only)
    1. Open Accessibility Inspector
            - Need to have Xcode installed.
    1. Access your device
        1. Plug the mobile device to your computer
        1. On the top left corner of the open window, select the desired device
        1. On the top left corner of the open window, next to the device name, select "All processes"
        1. On your device, launch the application that you intend to inspect
        1. Inspect Elements:
            1. On the Accessibility Inspector window, the forth symbol from right-to-left on the top right corner. Tap over the `Start Inspection Follows Point` symbol.
            1. Then on your application, tap over the element you wish to inspect
            1. The Accessibility Inspector should give all the information regarding that element
1. UIAutomator Viewer (Android only)
    1. Executing Uiautomator Viewer
        1. Plug the mobile device to your computer
        1. On your terminal, make sure you're on the users directory
        1. Then type ```$ cd your_path_to_android_sdk/tools/``` and press Enter
        1. The type ```$ uiautomatorviewer``` and press Enter
        1. Inspect App Elements:
            1. With the UIautomator Viewer open, tap over `Device Screenshot` button
            1. A image from the app should be visible and it should be possible to select and inspect each element from the app screen

### Desired Capabilities
<details>
  <summary>Android</summary>

```json
            {
                "platformName": "Android",
                "platformVersion": "VersionNumber",
                "deviceName": "DeviceName",
                "udid": "DeviceUdID",
                "app": "/Users/username/project_name/core_files/resources/apps/android_app.apk",
                "appPackage": "com.app.package",
                "appActivity": "com.arctouch.MainActivity",
            }
```
</details>

<details>
<summary>iOS</summary>

```json
            {
                "platformName": "iOS",
                "platformVersion": "VersionNumber",
                "deviceName": "DeviceName",
                "automationName": "XCUITest",
                "app": "/Users/username/project_name/core_files/resources/apps/ios_app.ipa",
                "udid": "DeviceUdID",
                "xcodeOrgId": "5HMJW6N276",
                "xcodeSigningId": "iPhone Developer",
                "bundleIdentifier": "com.bundle.id"
            }
```
</details>

## Android packages

- Java: https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html
- Android SDK: https://developer.android.com/studio

## iOS packages

- Carthage:
```brew install carthage```
- Appium setup for Real Devices: http://appium.io/docs/en/drivers/ios-xcuitest-real-devices/

## Tag Counter Reporter

Tag Counter Reporter provides a way to count how many scenarios tagged as @Automation, @Automation_TBD and @Manual tags we have in a Feature file.

To execute:

- For all feature files:
```$ python tag_count.py --all```

- For a specific feature file:
```$ python tag_count.py --f Test.feature```

# SauceLabs Build Uploader

There is a Python script to help us upload the application files to SauceLabs file storage on [core_files/support/saucelabs/upload_apps.py](upload_apps.py).

The SauceLabs credentials should be baked in the environment. To make that happen, run the following commands:

- For username:
```$ export $SAUCE_USERNAME="your_username"```

- For access key:
```$ export $SAUCE_ACCESS_KEY="your_access_key"```

To run the uploader, make sure that you're in the correct folder.

- For Android builds, run:
```$ python upload_apps.py --p android --n prefix```

- For iOS builds, run:
```$ python upload_apps.py --p ios --n prefix```

The N flag is used to specify the prefix for the application name inside the SauceLabs file storage. You need to make sure that its name is the same as the application name in the [core_files/resources/apps](apps) folder and [core_files/resources/app_config.yml](app_config.yml) file.

By default, this script uploads the builds from [core_files/resources/apps](apps) folder, if you want to specify a custom path, use the following:

```$ python upload_apps.py --p ios --l /Users/username/Desktop/ios.ipa```

In case of questions about the uploader script, run:

```$ python upload_apps.py --help```
