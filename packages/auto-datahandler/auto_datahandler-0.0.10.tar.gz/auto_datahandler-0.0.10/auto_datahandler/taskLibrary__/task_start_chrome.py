from basement__.ContralSelenium import Base_Selenium
from basement__.ContralerDatabase import Contraler_Database
def start_chrome(chromeDriverPath):
    c = Base_Selenium()
    driver = c.init_webdriver(chromeDriverPath=chromeDriverPath)
    executor = driver.command_executor._url
    session_id = driver.session_id
    print("driver executor : ", executor)
    print("driver session id: ", session_id)
    return {
        "executor": executor,
        "session_id": session_id
    }
c = Base_Selenium()
driver = c.init_webdriver(chromeDriverPath=r'E:\Projects\webDriver\chrome\chromedriver.exe')
dbOperator = Contraler_Database(databaseName='data_usable_database')
executor = driver.command_executor._url
session_id = driver.session_id
sql_update = 'UPDATE `data_usable_database`.`tb_selenium_info` SET `executor` = \'{}\', `session_id` = \'{}\' WHERE (`id` = \'1\');'.format(
    executor,
    session_id
)
dbOperator.cursor.execute(sql_update)
print("driver executor : ", executor)
print("driver session id: ", session_id)

