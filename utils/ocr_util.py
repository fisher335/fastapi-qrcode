# coding:utf-8
import os

from aip import AipOcr


class OcrClient:
    """ 你的 APPID AK SK """
    APP_ID = '16667601'
    API_KEY = 'T3xjr0oIM7Pv6cOBU4N6cn90'
    SECRET_KEY = 'IK4bMvckG5yMYEAswKRYeGGFlfQddUlV'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    """ 读取图片 """

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def simple_ocr(self, path):
        result = self.client.basicGeneral(self.get_file_content(path))
        words = ""
        if result.get('log_id', '') != "":
            for i in result.get('words_result'):
                words += i['words'] + '''<br>'''
        else:
            words = str(result)
        return words

    def hello(self):
        return "hello java"

    def fapiao(self,file_path):
        options = {}
        options['type'] = 'normal'
        result = self.client.vatInvoice(open(file_path, 'rb').read(), options=options)
        print(result)
        if "error_code" in result.keys():
            print(result["error_code"])
            return result["error_code"]
        else:
            ticket = result['words_result']

            print(ticket)
            print('合计金额', ticket['TotalAmount'])
            print('合计税额', ticket['TotalTax'])
            print('平均税率', format(float(ticket['TotalTax']) / float(ticket['TotalAmount']) * 100, '0.2f') + '%')
            print('价税合计', ticket['AmountInWords'])
            print('价税合计', ticket['AmountInFiguers'])
            print()
            print('销售方名称', ticket['SellerName'])
            print('销售方纳税人识别号', ticket['SellerRegisterNum'])
            print('销售方地址及电话', ticket['SellerAddress'])
            print('销售方开户行及账号', ticket['SellerBank'])
            print()
            print('购方名称', ticket['PurchaserName'])
            print('购方纳税人识别号', ticket['PurchaserRegisterNum'])
            print('购方地址及电话', ticket['PurchaserAddress'])
            print('购方开户行及账号', ticket['PurchaserBank'])
            print()
            print('收款人', ticket['Payee'])
            print('复核', ticket['Checker'])
            print('开票人', ticket['NoteDrawer'])
            print('开票日期', ticket['InvoiceDate'])
            return ticket
        os.remove(file_path)


if __name__ == '__main__':
    oc = OcrClient()
    oc.fapiao()
