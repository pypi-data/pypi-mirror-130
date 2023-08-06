from th_txmessage.tx_ms_utils import TxYunMessageUtils
import traceback
import json
import time;

class TxyunMessage:
    message_deal_process = {}
    
    def message_deal(self, messageType):
        def wrap(func):
            self.message_deal_process[messageType] = func
            return func
        return wrap

    def __init__(self, qname, secretId, secretKey) -> None:
        self.qname = qname
        self.secretId = secretId
        self.secretKey = secretKey
        txyunUtils = TxYunMessageUtils(self.secretId, self.secretKey)
        self.txyunUtils = txyunUtils;

    def listent(self):
        while True:
            try:
                myQueue = self.txyunUtils.getQueue(self.qname)
                recv_msg = myQueue.receive_message(30)
            except Exception as e:
                time.sleep(30)
            else:
                try:
                    messageBody = json.loads(recv_msg.msgBody)
                    if "lx" not in messageBody.keys() or "data" not in messageBody.keys():
                        myQueue.delete_message(recv_msg.receiptHandle)
                    else:
                        flag = self.run(
                            message_type=messageBody["lx"], message_body=messageBody["data"])
                        if flag == True:
                            myQueue.delete_message(recv_msg.receiptHandle)
                except Exception as e:
                    time.sleep(5);
                    traceback.print_exc()

    def run(self, message_type, message_body):
        if message_type in self.message_deal_process.keys():
            return self.message_deal_process[message_type](message_body)
