FROM harbor.huaun.com:11443/ai.scan/vul-pocsuite:0.0.0
COPY ./pyServer /pocsuite
CMD [ "/python/bin/python","/pocsuite/server.py","-p","50051"]
