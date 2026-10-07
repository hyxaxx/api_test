from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "pages" / "login.html"


@pytest.fixture
def driver():
    d = webdriver.Chrome()
    d.implicitly_wait(5)          # 找不到元素时最多等 5 秒
    yield d
    d.quit()                      # 收尾一定要关，不然浏览器越开越多


def _open(driver):
    driver.get(PAGE.as_uri())      # as_uri() 把本地路径转成 file:/// 形式

@pytest.mark.ui
def test_login_success(driver):
    _open(driver)
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("123456")
    driver.find_element(By.ID, "submit").click()

    assert driver.find_element(By.ID, "message").text == "登录成功"

@pytest.mark.ui
def test_login_wrong_password(driver):
    _open(driver)
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("wrong")
    driver.find_element(By.ID, "submit").click()

    assert driver.find_element(By.ID, "message").text == "用户名或密码错误"