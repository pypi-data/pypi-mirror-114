import time
from datetime import datetime

import requests
import wget
import zipfile
import os

from jsmin import jsmin
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver

now = datetime.now()
timeout = 1000

minified = jsmin("""
window.pybancodobrasil = {
    extratos: {
        counter: 0,
        results: [],
        methods: {
            goto: () => {
                document.querySelector('[codigo="32456"]').click()
            },
            get: (month, year) => {
                window.pybancodobrasil.extratos.counter++;
                $.ajaxApf({
                    atualizaContadorSessao: true,
                    cache: false,
                    funcaoSucesso: (data) => {
                        try {
                            if (data) {
                                const table = $(data).find('table#tabelaExtrato')[0]
                                if (table)
                                    window.pybancodobrasil.extratos.results = [...window.pybancodobrasil.extratos.results, ...window.pybancodobrasil.extratos.methods.table2Json(table)];
                            }
                        } catch (error) {
                        }
                        window.pybancodobrasil.extratos.counter--;
                    },
                    funcaoErro: () => {
                        window.pybancodobrasil.extratos.counter--;
                    },
                    parametros: {
                        ambienteLayout: "internoTransacao",
                        confirma: "sim",
                        periodo: `00${month.padStart(2, '0')}${year}`,
                        tipoConta: "",
                        novoLayout: "sim"
                    },
                    simbolo: "30151696898430647187469639762490",
                    tiporetorno: "html",
                    type: "post",
                    url: "/aapf/extrato/009-00-N.jsp"
                })
            },
            table2Json: (table) => {
                var data = [];
                for (var i = 1; i < table.rows.length; i++) {
                    var tableRow = table.rows[i];
                    var rowData = [];
                    for (var j = 0; j < tableRow.cells.length; j++) {
                        rowData.push(tableRow.cells[j].innerText);;
                    }
                    data.push(rowData);
                }
                for (let index in data) {
                    if (data[index].length < 4) {
                        delete data[index];
                    } else {
                        if (!data[index][4]) {
                            delete data[index]
                        }
                    }
                }
                return window.pybancodobrasil.extratos.methods.parse(data.filter(item => item));
            },
            parse(array) {
                const parsed = [];
                for (let [data, a, descricao, b, valor] of array) {
                    const [strvalor, cd] = valor.split(' ');
                    value = parseFloat(strvalor.replace('.', '').replace(',', '.')) * (cd == 'C' ? 1 : -1)
                    const [dd, mm, yyyy] = data.split('/');
                    if (descricao != 'Saldo Anterior') {
                        parsed.push({
                            date: new Date(`${yyyy}-${mm}-${dd}`),
                            value,
                            description: descricao
                        })
                    }
                }
                return parsed;
            },
        }
    },
    faturas: {
        cartoes: [],
        done: false,
        methods: {
            goto: () => {
                document.querySelector('[codigo="32715"]').click()
            },
            cartoes: () => {
                return document.querySelector('#carousel-cartoes').childElementCount;
            },
            faturas: () => {
                return document.querySelectorAll('[indicetabs]').length;
            },
            buscaFaturas: (indice) => {
                var url = "/aapf/cartao/v119-01e2.jsp?indice=" + indice;
                var req = configura();
                req.open("GET", url, true);
                req.onreadystatechange = function () {
                    if (req.readyState == 4) {
                        let len = $(req.responseText).find('li').size();
                        window.pybancodobrasil.faturas.methods.buscaExtrato(indice, 0, len, () => {
                            if ((indice + 1) < window.pybancodobrasil.faturas.methods.cartoes()) {
                                window.pybancodobrasil.faturas.methods.buscaFaturas(indice + 1)
                            } else {
                                window.pybancodobrasil.faturas.done = true
                            }
                        })

                    }
                };
                req.send(null);
            },
            buscaExtrato: (cartao, ind, len, fnEnd) => {
                var indice = ind;
                try {
                    var url = "/aapf/cartao/v119-01e3.jsp?indice=" + indice + "&pagina=normal";
                    var req = configura();
                    req.open("GET", url, true);
                    req.onreadystatechange = function () {
                        if (req.readyState == 4) {
                            const result = window.pybancodobrasil.faturas.methods.parse(req.responseText)
                            if (result && result.values.length) {
                                if (!window.pybancodobrasil.faturas.cartoes[cartao]) {
                                    window.pybancodobrasil.faturas.cartoes[cartao] = []
                                }
                                window.pybancodobrasil.faturas.cartoes[cartao].push(result)
                            }
                            if ((ind + 1) < len) {
                                window.pybancodobrasil.faturas.methods.buscaExtrato(cartao, ind + 1, len, fnEnd);
                            } else {
                                fnEnd();
                            }
                        }
                    };
                    req.send(null);
                } catch (e) {
                }
            },
            table2Json: (table) => {
                var data = [];
                for (var i = 1; i < table.rows.length; i++) {
                    var tableRow = table.rows[i];
                    var rowData = [];
                    for (var j = 0; j < tableRow.cells.length; j++) {
                        rowData.push(tableRow.cells[j].innerText);;
                    }
                    data.push(rowData);
                }
                for (let index in data) {
                    if (data[index].length < 4) {
                        delete data[index];
                    } else {
                        if (!data[index][3] || data[index][0] == "R$ ") {
                            delete data[index]
                        }
                    }
                }
                return window.pybancodobrasil.faturas.methods.parseValues(data);
            },
            parseValues(array) {
                const values = [];
                for (let data of array) {
                    try {
                        const [dd, mm] = data[0].split('/');
                        const description = data[1]
                        const tvalue = data.length == 5 ? data[4]: data[3]
                        const value = parseFloat(tvalue.replace('.', '').replace(',', '.')) * -1;
                        const date = new Date(`2021-${(parseInt(mm) + '').padStart(2, '0')}-${dd}`)
                        if (!value || isNaN(date.getTime())) {
                            continue;
                        }
                        values.push({
                            date,
                            description,
                            value,
                        })
                    } catch (e) { }
                }
                return values;
            },
            last: {

            },
            parse: (data) => {
                const $el = $(data).find('.textoIdCartao')[1]
                if (!$el) {
                    return;
                }
                const cardNumber = $(data).find('.textoIdCartao')[1].innerText;
                const tables = $(data).find('table').toArray()
                let values = [];
                for (const table of tables) {
                    const nvalues = window.pybancodobrasil.faturas.methods.table2Json(table);
                    if (nvalues && nvalues.length)
                        values = [...values, ...nvalues];
                }
                let dd = 01;
                let mm = 01;
                let yyyy = 2021;
                $elVencimento = $(data).find('.vencimentoFatura')[0]
                if ($elVencimento){
                    $($elVencimento).children('span').remove();
                    const [ddd, mmd, yyyyd] = $elVencimento.innerText.trim().split('/');
                    dd = ddd;
                    mm =  mmd;
                    yyyy = yyyyd;
                    window.pybancodobrasil.faturas.methods.last.dd = dd;
                    window.pybancodobrasil.faturas.methods.last.mm = mm;
                    window.pybancodobrasil.faturas.methods.last.yyyy = yyyy;
                } else {
                    if (window.pybancodobrasil.faturas.methods.last.dd) {
                        dd = window.pybancodobrasil.faturas.methods.last.dd;
                        mm = parseInt(window.pybancodobrasil.faturas.methods.last.mm)+1;
                        yyyy = window.pybancodobrasil.faturas.methods.last.yyyy;
                        if (mm == 13){
                            mm = 1;
                            yyyy++;
                        }
                    }
                }
                return {
                    values,
                    cardNumber,
                    date: new Date(`${yyyy}-${(mm+'').padStart(2, '0')}-${dd}`)
                }
            }
        }
    }
}
""")


def __login(driver, agencia, conta, senha):
    driver.get("https://www2.bancobrasil.com.br/aapf/login.html?1624286762470#/acesso-aapf-agencia-conta-1")
    WebDriverWait(driver, timeout).until(
        expected_conditions.visibility_of_element_located((By.ID, "dependenciaOrigem")))
    driver.find_element(By.ID, "dependenciaOrigem").send_keys(agencia)
    WebDriverWait(driver, timeout).until(
        expected_conditions.visibility_of_element_located((By.ID, "numeroContratoOrigem")))
    driver.find_element(By.ID, "numeroContratoOrigem").send_keys(conta)
    driver.find_element(By.ID, "botaoEnviar").click()
    WebDriverWait(driver, timeout).until(
        expected_conditions.visibility_of_element_located((By.ID, "senhaConta")))
    driver.find_element(By.ID, "senhaConta").send_keys(senha)
    try:
        driver.find_element(By.ID, "botaoEnviar").click()
    except Exception as err_button_sent:
        print('Possible not an error - button sent', __login.__name__, err_button_sent)
    time.sleep(3)
    WebDriverWait(driver, timeout).until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".menu-completo > .menu-itens")))


def __extratos(driver, fromyear=1993):
    try:
        time.sleep(1)
        driver.execute_script(minified)
        driver.execute_script("window.pybancodobrasil.extratos.methods.goto()")
        time.sleep(1)
        for year in range(fromyear, now.year + 1):
            for month in range(1, 13):
                if year == now.year and month > now.month:
                    break
                driver.execute_script(
                    'window.pybancodobrasil.extratos.methods.get(\'' + str(month) + '\', \'' + str(year) + '\')')
        counter = 1
        while counter > 0:
            counter = driver.execute_script('return window.pybancodobrasil.extratos.counter')
            time.sleep(0.3)
        time.sleep(1)
        return driver.execute_script('return window.pybancodobrasil.extratos.results')
    except Exception as error:
        print('Error', __extratos.__name__, str(error))
    return []


def __faturas(driver):
    try:
        driver.execute_script(minified)
        driver.execute_script("window.pybancodobrasil.faturas.methods.goto()")
        time.sleep(1)
        driver.execute_script("window.pybancodobrasil.faturas.methods.buscaFaturas(0)")
        done = False
        while not done:
            done = driver.execute_script('return window.pybancodobrasil.faturas.done')
        time.sleep(1)
        return driver.execute_script('return window.pybancodobrasil.faturas.cartoes')
    except Exception as error:
        print('Error', __faturas.__name__, str(error))
    return []


def __cdb(driver):
    driver.execute_script(minified)
    try:
        driver.execute_script("document.querySelector(\'[codigo=\"33130\"]\').click()")
        WebDriverWait(driver, timeout).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "#botaoContinua")))
        driver.find_element(By.ID, "botaoContinua").click()
        WebDriverWait(driver, timeout).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "#botaoContinua2")))
        driver.find_element(By.ID, "botaoContinua2").click()
        WebDriverWait(driver, timeout).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".transacao-corpo  table:nth-child(6)")))
        lines = driver.find_element(By.CSS_SELECTOR,
                                    ".transacao-corpo  table:nth-child(6)").find_elements_by_css_selector('tr')
        for line in lines:
            if "Saldo liquido projetado" in line.get_attribute('innerText').replace('\xa0', ' '):
                non_blank_items = list(
                    filter(lambda s: s != "", line.get_attribute('innerText').replace('\xa0', ' ').split(' ')))
                replaced_items = list(
                    map(lambda s: s.replace('\n', '').replace('\t', '').replace('.', '').replace(',', '.'),
                        non_blank_items))
                return float(replaced_items[len(replaced_items) - 1])
    except Exception as error:
        print('Error', __cdb.__name__, str(error))
    return None


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    if os.path.isfile('chromedriver.exe'):
        return webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
    url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
    response = requests.get(url)
    version_number = response.text
    download_url = "https://chromedriver.storage.googleapis.com/" + version_number + "/chromedriver_win32.zip"
    latest_driver_zip = wget.download(download_url, 'chromedriver.zip')
    with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
        zip_ref.extractall()
    os.remove(latest_driver_zip)
    return webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)


def get(agencia, conta, senha):
    driver = get_driver()
    __login(driver, agencia, conta, senha)
    retorno = {
        'transactions': __extratos(driver, 1993),
        'cards': __faturas(driver),
        'cdb': __cdb(driver)
    }
    driver.quit()
    return retorno
