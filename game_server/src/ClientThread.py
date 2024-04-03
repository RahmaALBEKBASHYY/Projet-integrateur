import threading


class ClientThread(threading.Thread):

    def __init__(self,Client_code):

        threading.Thread.__init__(self)
        self.Client_code = Client_code
        self.client_login = ""

        
    """
    @brief: run gère un client du début à la fin
    @input: self, le thread du client
    @output: 0, tout est bien qui finit bien
    """
    def run(self):
        print("run")