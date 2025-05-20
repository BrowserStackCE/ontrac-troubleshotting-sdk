import os
import yaml
import logging
import sys
from Utilities.common_util import CONFIG_PATH
from Utilities.read_properties import read_config_data, read_platforms
import configparser


# You'll need to import or define these functions:
# from your_module import file_path, read_config_data, read_platforms

def main(markexpr=None):
    try:
        config = configparser.ConfigParser()
        config.read(os.path.abspath('.') + "\\" + "Configurations\\config.ini")
        if markexpr == 'android' or not markexpr:
            config['Android1_BrowserStack']['device_name'] = os.getenv('device_name')
            config['Android1_BrowserStack']['os_version'] = os.getenv('os_version')
            config['browserstack']['android_app'] = os.getenv('browserstack_app_id')
            with open(os.path.abspath('.') + "\\" + "Configurations\\config.ini", 'w') as configfile:
                config.write(configfile)
        elif markexpr == 'ios':
            print('IOS')
        else:
            logging.getLogger("root").warning(f"No matching mark expression: {markexpr}")
    except:
        pass

    yaml_file = os.path.join('browserstack.yml')
    if os.path.exists(yaml_file):
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file) or {}
    else:
        data = {}
    browserstack_config = read_config_data(CONFIG_PATH, 'browserstack')

    try:
        if markexpr == 'android' or not markexpr:
            data['app'] = browserstack_config['android_app']
            data['platforms'] = read_platforms(CONFIG_PATH, 'Android')
            data['userName'] = os.getenv('Browserstack_userName')
            data['accessKey'] = os.getenv('Browserstack_accessKey')
            logging.getLogger("root").info("Successfully changed Yaml file to Android Config")
        elif markexpr == 'ios':
            app_url = browserstack_config['ios_app']
            data['app'] = app_url
            data['platforms'] = read_platforms(CONFIG_PATH, 'ios')
            logging.getLogger("root").info("Successfully changed Yaml file to iOS Config")
        else:
            logging.getLogger("root").warning(f"No matching mark expression: {markexpr}")

    except KeyError as e:
        logging.getLogger("root").error(f"KeyError: {e}. Please check the configuration in the config.ini file.")
        raise
    except ValueError as ve:
        logging.getLogger("root").error(f"ValueError: {ve}. Please update the app capability with a valid value.")
        raise

    with open(yaml_file, 'w') as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False, indent=2)


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Get markexpr from command line arguments if provided
    markexpr = sys.argv[1] if len(sys.argv) > 1 else None

    main(markexpr)
