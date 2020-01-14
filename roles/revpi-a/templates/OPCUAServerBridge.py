import logging
from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.handler import LogstashFormatter
import asyncio
from asyncua import ua, Server
from socket import socket, AF_INET, SOCK_STREAM

#Bridge variables
bridge_open_string = "[SYS:1]"
bridge_close_string = "[SYS:2]"
bridge_reset_string = "[SYS:3]"
ip_port = "192.168.10.10"

#logstash logger
# Create the logger and set it's logging level
logger = logging.getLogger("logstash")
logger.setLevel(logging.INFO)
# Create the handler
handler = AsynchronousLogstashHandler(
    host='172.16.1.3',
    port=5000,
    ssl_enable=False,
    ssl_verify=False,
    database_path='')
# Here you can specify additional formatting on your log record/message
formatter = LogstashFormatter()
handler.setFormatter(formatter)
# Assign handler to the logger
logger.addHandler(handler)
# Send log records to Logstash
logger.info('Started OPCUA-Server script.')

async def main():
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    # setup our own namespace, not really necessary but should as spec
    uri = "http://alex.freeopcua.github.io"
    idx = await server.register_namespace(uri)
	# set certificate and private key
    await server.load_certificate("cert.der")
    await server.load_private_key("private.pem")
	# set all possible endpoint policies for clients to connect through
    server.set_security_policy([
        #ua.SecurityPolicyType.NoSecurity
        ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt
        # ua.SecurityPolicyType.Basic256Sha256_Sign,
    ])
    objects = server.get_objects_node()
    myobj = await objects.add_object(idx, 'light')
    # populating our address space
    myvar = await myobj.add_variable(idx, 'bridgeState', 0)
    # Set MyVariable to be writable by clients
    await myvar.set_writable()
	# Setup connection to bridge
	sock = socket(AF_INET, SOCK_STREAM)
    try:
        sock.connect(ip_port)
    except Exception as e:
        logger.error(f"Failed to connect: {e}")
		
    currentbridgeState = 0;
    print('started server')
    async with server:
        while True:
            await asyncio.sleep(1)
            bridgeState = await myvar.get_value()
            if currentbridgeState != bridgeState:
               currentbridgeState = bridgeState
               logger.info('Changed bridgeState to ' + str(bridgeState))
			   if bridgeState == 0:
                  try:
                      sock.send(str.encode(bridge_close_string))
                      logger.info("Bridge is closing")
                  except Exception:
                      logger.error("Bridge is closing error")
               elif bridgeState == 1:
                  try:
                      sock.send(str.encode(bridge_open_string))
                      logger.info("Bridge is opening")
                  except Exception:
                      logger.error("Bridge is opening error")
			   elif bridgeState == 2:
                  try:
                      sock.send(str.encode(bridge_reset_string))
                      logger.info("Bridge is resetting")
                  except Exception:
                      logger.error("Bridge is resetting error")

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    #loop.set_debug(True)
    loop.run_until_complete(main())
    loop.close()
