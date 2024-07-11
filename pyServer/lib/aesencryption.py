# -*- coding: utf-8 -*-
import argparse
from binascii import b2a_hex, a2b_hex

from Crypto.Cipher import AES


# from Crypto import Random


class AesEncryption(object):
    def __init__(self, key, mode=AES.MODE_CFB):
        self.key = self.check_key(key)
        # 密钥key长度必须为16,24或者32bytes的长度
        self.mode = mode
        # self.iv = Random.new().read(AES.block_size)
        self.iv = b'\xbf\xe7\x87\xa9N\xf7\xc8\xa7\xd7\x94F\x91p-\t\xa4'

    def check_key(self, key):
        '检测key的长度是否为16,24或者32bytes的长度'
        try:
            if isinstance(key, bytes):
                assert len(key) in [16, 24, 32]
                return key
            elif isinstance(key, str):
                assert len(key.encode()) in [16, 24, 32]
                return key.encode()
            else:
                raise Exception(f'密钥必须为str或bytes,不能为{type(key)}')
        except AssertionError:
            print('输入的长度不正确')

    def check_data(self, data):
        '检测加密的数据类型'
        if isinstance(data, str):
            data = data.encode()
        elif isinstance(data, bytes):
            pass
        else:
            raise Exception(f'加密的数据必须为str或bytes,不能为{type(data)}')
        return data

    def encrypt(self, data):
        ' 加密函数 '
        data = self.check_data(data)
        cryptor = AES.new(self.key, self.mode, self.iv)
        return b2a_hex(cryptor.encrypt(data)).decode()

    def decrypt(self, data):
        ' 解密函数 '
        data = self.check_data(data)
        cryptor = AES.new(self.key, self.mode, self.iv)
        return cryptor.decrypt(a2b_hex(data)).decode()


if __name__ == '__main__':
    import os

    def cmd_parser():
        try:
            parser = argparse.ArgumentParser()
            parser.add_argument(dest="files", nargs="?", help="文件或目录")
            parser.add_argument("--key", "-k", dest="key", default='huaun666huaun666', nargs="?",
                                help="必须为16、24、32位数字加字母 -k qweqweqweqweqweq")
            parser.add_argument("--ext", "-e", dest="ext", default='un', nargs="?", help="指定生成后缀名 -e txt")
            parser.add_argument("--name", "-n", dest="name", nargs="?", help="指定生成后文件夹 -n dir")
            arg = parser.parse_args()
            return arg
        except:
            pass


    target = cmd_parser().__dict__

    files = target.get("files")
    key = target.get("key")
    ext = target.get("ext")
    name = target.get("name") if target.get("name") else files + "_bak"


    def read_file(file):
        with open(file, "rb") as f:
            data = f.read()
        return data


    def write_file(file, data):
        try:
            with open(file, 'w') as f:
                f.write(data)
                print(f'生成文件{file}')
        except Exception as e:
            print(f"生成文件{file}失败 {e}")


    def exec_aes(files, type):
        aes = AesEncryption(key)

        if type == "dir":
            if not os.path.exists(name):
                os.mkdir(name)
                print(f"创建文件夹{name}")
            for root, dirs, fs in os.walk(files):
                for dir in dirs:
                    if dir.startswith('__'): continue
                    dir_path = os.path.join(root, dir).replace(files, name, 1)
                    if not os.path.exists(dir_path):
                        os.mkdir(dir_path)
                for file in fs:
                    if str(file).startswith('__'): continue
                    file_path = os.path.join(root, file)
                    data = read_file(file_path)
                    e = aes.encrypt(data)
                    new_name = file_path.replace('.py', '.un').replace(files, name, 1)
                    write_file(new_name, e)

        elif type == "file":
            data = read_file(files)
            e = aes.encrypt(data)
            new_name = files.replace('.py', '.un')
            write_file(new_name, e)

    # 判断是单个文件还是目录
    # if os.path.isdir(files):
    #     exec_aes(files, type="dir")
    # elif os.path.isfile(files):
    #     exec_aes(files, type="file")
    # else:
    #     print("输入正确的文件或目录")

    # key = "huaun666huaun666"
    # with open(os.path.join(os.getcwd(), "test.py"), "rb") as f:
    #     data = f.read()
    # print(data)
    # aes = AesEncryption("huaun666huaun666")
    # e = aes.encrypt(data)  # 调用加密函数
    # e = "4abe7b56cd2dc115b9ef139ab75c434e6c46926bb8a96202b21ea9eae1556dae7c3f4ad4698ad4d0d75a7f0b04734af2eef517ae2d9a378b35d0444a62db308867f2be6243a521ccefac5948cd192a7269d9e8d2c7c3dcb2e241e934d01f60d4675374ee6a7d4740e2765c61f9842cc73c056e21d0f65a6875af52b0af4adb22bd6bfb6fa0ea56ae529434251265d59338005a02d48a5f8ce712bb7580bd004a09f159ce0390b397c5a698848f2b1281f03f65fa1dae3f5a9205a2173c8e9c1310a92c26677a4f8e19dba09bf68c090a6e0bb02a8d98b240f2d916211c40177b2a92516530350d35a9209f8b53dc6fe7fab5513341503ffdc0ceb04ddc21854643e951636c81d5f5ba370a85e163dd154a0a160d0bf3412d2f0e79cb5e4b41a15d915659f50b6ab1eca61c1feeefbd55c87d8b8c205ae01e35e1787892da60e6a00867503b18f24a1f79d293fb506c8cb38fec81f818eec37b8c36981b6b33b1392046ecdda0f783e19fc3e9549fe9c0725a03579471586c3346a30c61b89242e0e55003ed6a87460f6db9b16e646969ae8adc99b8c75610580704f0e72efb83d8b162ec81b4ca4de81a5c40972986b75fd3474cd1fdc57410dd7370889d858aa872f4037109a6b638100f6b7d642a7f6c9a64c965fa52e83fb56ef679d4652f37119725caa50da3cdca2a05b4a9d5a2ac27d051abe4348b7a855ef1f0a7e7ec661c9103be57544949868eb0b04dd2015d33122178925e17d106247efcfd33bca3550a4a123f7ea0abefdeeddd14e5bb1ad87579593437f754bc7c8f2a56876122fb7c456f0dfaccefc144107eb620c1e9e4b646e5c9e03da55dadd0573980cd90a2db0b4ed3f003d971fef4ed74b4c75c459b9cc7a8a02dd0ad0383a2e19ab1f819ce9d8d442eb9e417a1530419f0339765fd768e6cec6f1e33bd88103f53f441cae50775550bcdaf07de4c100fce1aa193ff5d15157723adb0fb7338ce7f37a922dd52c4ed840188fe28ba923f9dd68e52154e5d212e10b63f0cca0fff344b5ae7468dc66ae28a0a6cb21373d638074722100c4318c6a5a5103fd23009b25fec09a7c95e0059acba35b69bb6c42ab88b6e4a747cb263e413f1307f3cd7486c2011303e722dc176199ffd219516e90be383a4d8f0527dca94433bcebfad5742cf7763fb65a5b142e766fd55060696f2380505eb24cebc5bafeb5c820ca3a61572ace2e0b287d8e2d156d13102fb81fe0f032fde78af0df088da06e6f78cbecc7ade91c2fbb4f35585fd694ee45b1a628ba43e41541839c729a876bf13d9959442dcffe5235bb8743a177a5c3159159901acf0064616831519b281a8ef906c804e7bea01d4dfe50bbafea3c96fcd6e883f41b2ca009faf79645a0086ea0615bdf3ada7f80b02d66c0aeb683793bcfeb05fb5e3e813809006824f176e6bb3225db98d62a73004753ddda26f322cd93209b6968c0dda3a2546835109eae7a282b546226476aa9e20e2e1de8bd4cc35241c59981ab76f4e8b5afd8d2c75806830bc22bd615179786ee73354557093af32a9fe44ab9cc794af158d1e474e5659947e07f8b634d1c54ed0cba63b4963ff15366bb27d1a1ecf308aa5d7ba19d85cc5dd81b4dfda165c5a5145a2dc42c723360ed235fecb1ac6cc22439320b4ad4dba9a1c48d8e57e759e883f720171fd24c18b514919a42d77084c9614de582df2775ff24e5650fd65eb15c64f51a132c92daf0b84d7f70f29e852e5ace753fac10610c47d11a79c0a32ce7fb8bc27003b732d5e26374babd6999b661c5ca10e89ce6c2154e7819e46e7a774596bb724eec208496eaad04437077bfeb3beca18807ba59374940654fd83c937aea57b58caeea25a4e255f5eca962f12b18545bbb69626a1c260bb14d2fe737cb8d7fb1da535f38f7c6cc4d862ff1e876c47a6a1965cae6b1553ccd9c53a754cf34dd385c3a65f1603229962ee67b9164ed12b214b606e924a6592ca1932c4e561d838557f2126c68d595da2b96707c071dc6ed743a66d92b408f05fed1083c75fc4f611e00ea397029aa55f94cb487f3c5f6f9480df8313b3e512b4879b7b471a29b7dff8624a8c3c4e6e9a402becdeb3d5e60883fe7a3cfa951e21135334f0d263e6eb3ae71d2b621b53ff553307c1a9d4d97465e06a2dacb26bb3219b610c38b5d3b91591afcac60f748a9277ce3d8fd111544295322d1d966fc7a730e441dd2c01dc6807870f6994820158cc3037df4b1eb41e059c0d936240169dd3661c14996485cf026c6997cb73753e4dd6446790f4540374fab8412b4fd8fced6fbcf13db91d9af9f6c36bbc07979df383c40bdf2c05126e5f581cf90022f1a9b814a8984aba14574dcffe1ea02778fc222947aba70b10c156fa6b957fc7e496b606eab806129147c7fd19374643209864daa7982afb7ababf0939eecdeb3c2d7b49a97bf3e5131a34dcee37462e3a6ae4db2cac6265aab28e9609d576778c4c8f4ced03a262577056ca6da1c100a36e4da2d1e8dbf6e646393e181347b9ae31883332afe06188475c5955029cc13f9c470d62c0ef134462387d3eaeccdddee2d6a94a5f19da2a231f0660f01e2024598e0bb2b8ab92e0d5cfdef2e87967a5dfce30bf39200b929c02e070f52ff54601a196eec9fb97936bd3b70df33826662e24be05d4f6ae901911580e9e4b7fc528740e3018c31f89e8f48efdeab3f9ed4bc31b9ccf4985e87adc1bbb821e59618d5bc70ad905421ef575762df4b3e2922a8a5e058b8c52f5d06afe90d5cdad7588c33c80600f5383241635948c7367428032fe7e74409cee3eb1f1a5681e17dd65e3a14249c301b17d9a3a9754bd630b2b0fecfd7dd4d4f3726d681ce1b98a30eddfb87f25bb6cf76aef060a8738a672287d9c98c3a9ab5987abbaf25b1501fca2324b8b5f6a301847dccf44579924d3d4cf5980b6a647bc535944c48e47079d2f95d51ecdc6e435d00f1b1d208389327dc725e310337c701511bab73843422e774674de684a1b0f0c758419a17e797c9702b995896b689c72c11c49c44d6f759a1faccf0bdfed54d285e0f567db2e98918204886cdb7bcccf29553ff224ed51348395d4f3bf8f8d4f9f83f336fa92c33d4fd2dbe4ea54aaa7698a96a57212c1cd2e0fd34204d42af4dce798b2838867a429345e71f8bfdac2c9eaf9ff8a4a5a45ea63babc14e7fc8fd7aeddf95a6190513154bfe2545d71183e48eed2dade374d5793f00de27a2e49bd185e9f7e6d234e696fa6652b35bb340d1ed46e7a48bb253dae5cc3628065ff018747c0f0bf5dc1eb53b709dc9bae7524cbb71a11ccef78540ee84f5afb715f7ab480e7d940c581f54cd9e83c327673ad6431ca26e777aaff5b04a89a0494823f68559df3522b9c86915b08bcbbe02312bba8c2873cbedb544d698f80a6a581aa74df00940525ba9136b79002fabb804ff7fe0a7b966e2b06311eeeef18050efb6140e1cab10b9a018100c9514516da76b8250dfd3391671d618c69f3782ae65565b691006b6760dbcb228171d404a847d3fe26388eae7d2914aba9db2a1a1df1c9fe5b382b59df3a08253cb1d896e51539098ce758324f57b8046e4df1e8f8f5dde50c8b77f7b1def2a40194b04a423d4c9c50f3ed989051103de35ee825e3f51e13a562d67ca3186190089c89eaba60cebd2f22c46cf2503ce335587d6720b3db5abb8e2bcc423896ea0aa9446b6f96de439abc2f0774c489d3923427bf8f28e5b8d17a459f84fd72f1ec1f6b43f0acdf00ac9da32eec8617f414a7a082a3d1a44d78ecfb4229ba6cab5d3409ef190a3a00d3de5e4d15f843dd5245235db90638362a744d438014fec5b570c70547e7d25370cb4ca814c7532758cad68399205b3b9b15bfe74e57337bccce8c072a1c2b61cc0530923e76101692f50e29f566078b627ffd28e4021ccb6517aa169cc33ddcb4f8c0edc5539fbc438a2ba3616074da75c59aed143f13e27be176b657dca965a627a6dce96de8930b631a040f51e07bf6b03167cb2e8f5a0d65c39febf5c41426afadc4cadbec446ef9d14486daec0c665cd6fead3114416f92b7a38af884677824f6782861860ac30fb8141c202e96d7ce5d7a92a337f5261cccd32652f1fcabfe61f8767f76e4609dda586bfa59789da09fe5e3fec57ba1b156fcae86a98f2737ddc297d2465c51b0bac645fc08be8619222d964a3de2c26fbc926185b637621f97173be72c9a644ac6781d774644936174d5f80c2dbeffd5e12b19a547af515759f79c4083256cd59aa2293ad4844b1303d80ab8a9b0677582ee16ce592e888015ea348410c55fa10b62722306747f50c4fc7b88010dd1e17788c9c38ece408af07584b35896d25d0a40eb4865f5b350860cab9e900e9303e9cf1ce320b5341a1743437cb51cf344074e0746740c17aa0b7cefbb0f924b8b83f3afae52e388ba0dcbf2fde8e6e815a2d343871ceb79452d7b4bebef16f9dc12637f5d256ea22fc7f057713270ae389c39fdd9948a0bf1027991f747afa9b656831a822bcc71f395d8f71f8cb9a6b38e5193cde50151542d56156c30b5ceb0b1ea10fb353f3123813d2e301d509132c18e64e2e61aa4b3874ce51c915b1d62debc140389c30e3d532c79987b3677fbb665aab4b077632fb7a29942dddf19765ea89dd2916b75af2a6677cbc62d1b55ffd4041414b7a0fc505c610339d8c99093067f785840f08bdf1eeadcdf57d3b61e2a048657c774bde47c9a1b7d1dd6de18beddee54145866ac1df759f157dd5b12358ec6e100dfbfec00cbfcbf3002f1dc2efc2ccccae7c6528faea068a7f884d8ec53b148b4c7f1d02f23ae81138673ab439756d765b1b1109c07573306acdadb18daa0ebdb534a3bbc71f8707e2e5880d02f9bd6799e73c1597117eaa444a5cc2e3138f402fa338206eacf55534d139111ee55833555b0bc8c2ad864b6d7fdddcbdfa3963207892a2da6f480a726d2e0f17bd02507ec0c4b1a7db1d0616a8d3b64956f166fc34257101e4b58471828a27b48b7551d72381a1deedcf04d6cf804d24b844ddd82c537f21ea9dacce841a4bfa99bfd3499a728264eaaa127d81e1d1ba22495c10ec47dc72278e283c7c450e043e95745e2421a0e274d14ff4fea2560320b25f75f7013aad01ea71ccd1d03e0211b266e5a5101c969e76f4b31700d082da7564c01d01ac83067fb4ac34cee873957634c008f22750acc41c80c4e82551fc37007186d9a2ac330c4ee7fbdba4bf0809b4a0eb9044a151e3200156bd39d7ee8f7639565c9ec5e9497530a779319f8a5db49da46336950bca930494fb4d25fa456d571a78aef722ca9cc6dcefe0207ffb8a871e460291257b95e5b4e325bda56ccbc4bec76763205bb4fda3e2c06e83a96f722dcbd9004c671ac2f9e0841986dc95e8a1cb82b6908fb587584fb833f73539cbb55a31f63b094b313b7f5d0e8446012e1e111c64d1f7db78f8d2db73e4a4c64c98d07e7460a2c604e9d6bb9cfd23ad1e876b7975b79ca552fdef15293be238dc16a80f011006441c31195793e99c13f02eb53bce3a3c5ae47424933d1d4e6f2065fce13a01edd2b271bc6c93541ad9677611b4e289cd843b9abcf1954c2f7e7cd18a7e34dcdd6843da926326e9f7af6b26e7527164b2038125d86140de9578ff14c4a5964c6ea8649aaeda9b0898d8b6f70bb2915c9cfbf52fa9450f860b88e4629b8be7f9f649e2965c189be63974673aadf0d13f291a12cf4e4bd1196a0e1238bb15ca494d3bc36d0ebc47fd7215c0e093d6cac58bc782990452acc9b56096f04d4316ea8b7ecb6d7545b8ea48bf59dea29234d990287a36f0a64d678d441f5e92005fe8a7e2951dfb458ae089233baa010a27e490528c72f4ded771ecbfb901badc65598f212dcfa8f60495cf9794a708890587d57752df6d98a1a82a410e967744b1f7ff3c4142e17863434234ddc39edcc4d2526ad1011dadb1b42d1ff61141a577c1dd10f4b6bf0565ba16d38453002819820b910ffa92679fb4d6db151bf9884a2d88ca50f82b545e25cd4ed0c99d17caa444f6451364c61b43645d1107091689de1ed2a5873e6791332206e2ea2598c5ec55f8f49626452602363f7a3a4b2786082bfdacae968b8804eb075bb660e676b0a7440a52af5ff02a74612b7d19abf8c35d8b400ea3b5e11d38f576c13226b5e75f9e9ea5c70ba78a1922b9bfe580e08e265a05f9bcf2316d37bdc11304ac40ace6b5bdc4c34c5e726dda3abff3210381d407ce6cfc87e600628a330aaba9884fc63f8e6df322878f0753a04ff1c316875450d1b05198e0d92ca0a3abac1b741619cc499b2a5902a13778cc9477d4e544b4e6af1e0af9569ffafac245a633e482a2e93097dc67eb1b17fc7fccfe34a0859219674fc0d1dddfc11f04cd7dd7b176ea2474a2a47b4e89d8bea99e7407e2c6bb053d3aa4f1d4398ef7ae05f5a3c8e4c57692f118d1f1baa62d1aa102000e36cd1c3d1dd931b5d6f718d01463bb739625ef999a52efefe2ae85d57b9302a35f1d8478f79158917b634788bf7fe87b63c2aa9d46ddc19dfeebb1ce1580f98dbef2b06ae0d0fd5a2f6091bb53b6b18b01636a4fd20afbf0f728f8ac3409e0ceb5fb5d08352e299743382f46f5bac91c3aa4f1cf6ac2e442518607266ab8e9ec8b8b58b9fc7419de7c11af22d4526827810f2803f8931fe8ccc1525fe333fa9160619929774180a4c997b7a396795e7f32fc96a07797eb20e74ea300368ce3ea11efcaeca4f586770c276422ad6f5f80a50bcc4ffe38cf1c5bfc2235be42d9cc8a587513f744c17b15d0cc7c8eb2e539b5a5411d15a835d760077999beec6f6914188a9cbff0791de4f882e333ff9457ef109228a59432c403263dfbef35d3553439b29fd8c4d26f36c8f04ba190298596fab6375b6b38c2c52159a440b137784dc7357381f41adc8c2426b4b716ce32ad4225b0bcc65f7c23132724f7e177a247fe724674b52904a49f5a7c3b7b60591b3086bf340e8a7fd34f48826b8caeceeda83534845c68caf7e44a08d4bb9515afbfaefaea75bf624d543a69e89d05ea3d835e9c05be107a5cf4c3b32952eaef1036822e0dab4094307f40fefbbaa9fb20e3af16c26157816b58656738e111ca62328776f29a635582ba3629813d949407042323547ef04bf6776b4c6b61e981b3c77feb53db1449656a8c1ec98f23bf54d5c10cdeb83a80d550d6bd071b947b21538eaa5f8093f05f6b3efdb6c689b3c665c96223919d956b0f68aabd1cae34f58fbb08687f269c39dd0f5a2fb11bdb1820a9c3d8b8ca1bd48ff9b4d44d7e6846598c8c4fc7eeaa27a08263298fe704d0fa6f4355a67edb6a1cf001bacdb12a9a000bc0721f3c885df4dd17e18a245e9f56b38d36b9e32dd44e1f875e5aeae18b175bb0f1af600a916d93e0da014daae631aa3ff26c3d8efd17ee8ad33dfc298db6c7ca10469ffbf0b87879baeb9b43b3e22f49353197f8db33dd23a19f19755889e2854c4163178104e90dfe8c630172daf827dd08ad2d49884f6753b6b8c46cf5f954916925e76c6742f0ea28cfb6a56098180bc160bf95d87169704f09f6c825996896756b7bd8cb669836def7f75e88f0b59ab3ace8c6177b621b667ebe2606319afbdc617e88fd168bca62c85d6fa43f4af84b106608c6bf2c81c96d93cf82f8841781fdd22a330bd28d3d5eea1b4998b88bb0925bdfe7372b24b519f48e403894d133af224148f49aedd7b45dd165baa448b80c243464f4ca95d64b780d26f35bf2eedc751f60f3c8a3b90a9150088a667d5c7fd0a3ddba5a03adb79efca31c6242ded4378b9aeb3f2fbce5817296ead246eeb370c05ebb2ba31a8c8608a5986b898b905e8b097c73882f2bbbfaf97073aca489d4c32dafee5a70845fef39bb8ed1f7abd502cae4e78070451c5473db3c0ea0935f814f1802ccfc4c93cf049415e589a1337451a3f6aa310c2592bc73ddf0930a715f1758dfeba421915b2290df66a13ef539177c3316c76511ffa29726f363e35552bba33d0a07aef2c8475fc4d71747c8d4f73253fdaa68c98dd89d5946a4b8945830b197a0e167af3d09f9611ca149af6bf9a1ccfd2e036cefdc262998f635362e61d9bc7c75f28b8f6cfeff54e27009aae21f1bda6ecd2da7eccffe1f6234a32726929665fe0c82ab8eebb57db65de4b99feef00072c986f0b61485ce69f7d5192e9ec35d0f569ad298f63ce9fed07ab456ae8b6a1045f58e499c3b4576ce37b92388254c08b068c5707637396b56013c0294d8cf26413bcb444461dce81c6063d0e8631d19864545bb1943687709b72b63ad2c24ef1442bd7952d2f237904b17f3a8a3aa59089c37b0c30e92b832d1d2bbbb06e246ca45811a9a13c7c4005bb60e676b1bdc0654280d539a239ed17f0e21c350a1721566ca5d5f3aa27b19a56aa255176f6beec152fd603483b457a23bc20a7ce581d6f27fa0156165c1a4095ba666c8c9749f6b43fb92192127d73b1e47e2c50713842b58475e89457a2b25e3b6c9b303d09e4991b5892a0a61892b03030bfa8eb00b3c4e7567c53d6dee0ed31bed637a1bb05328552f7c5808213462b49eb5d16799ee984b53930d597765942c4b9fb453c54062a29ea0b53dcfe8507151a76b9607560cf3f803ac418f6ff7c36e135ddeea1d48c249985b99e7e02461125fa5677e8b40096bcc89a63f359362fe7043ab642f2811f9d0f15d45ddac20b9dd13334ca33426fea2039b2cf4343287d656530e87d55513a18d2709e31acf6f20577c35efb466d759b55fd07b5fd72d97bd5eff87c7a8ad895953a29d92864e4cbcf8b491df234fd9d6cecd3f0751130742f8013795b4d70665b7c15084358703004360b040e41c1b663b5e342ba43019846c9e928f22ae27e27d004c7b0d3a2f9070b41a78254113d21590385af896086a22665ede014bdf75dbf915105dace03cd6e165b1c918ecae6bc22773230a0463bbc8c1fa260086eea79585b91027151d439bb4c8ee1cafcee1c364d0f56bf40405fef5b3bf09ac34d41663c8ef3a1c45e06b1d6bae31ce7d8674b4b8e354bc8d2af65b8028c32b13e92a1fb865d6904b16aeb9b67e6c52f597aad806b9e443f1380d049de2459f022d11de0e20fc73e1dfc429e3e2f69f8fe6f0ab6bd8d5306f1f8e48a091c0325d162979e6d9f3b3c96897732742a745488795a94ac21c26518f697b0cc6abe95c1e87a22f78253f641a2c05162ecd50603076af797fe0d16175dc2e8e692ac58696aca03679e4ec0376a9cb20d0443a41fa857f873885958e64d5b05db311abd07c5959ab56f3b5259b58f3388cb9f8cba24e5fc8594bad6ee52026300e31ada9c6b74bd03e5129ae7ce2704ed1049ee556723304f380ecf2294d971438bbe85c905f5aa13ef96e61fc54d7e964d914e9c732647542706d08226553e9106f4d498021c00b891f020b194f0409d4647c97ac0eda314db10923fb2e1060d1ed7cc0ad5f042a0d69fdd743454aa5e92be5b7a99ff4cde77f3358f53fb72a1326e7bdaa3c80ea77ad296c106faff910f94113d8d0fc0371e3dd04266215bfba4142d3c808f8f10f8d3ac252a63b0fa21430f95889467de0e79410a7d8e33c9f705479b60a0fe1599aa259da3b67faefd25ce991ea503e85ad259847f0a8cf7058bd67ea4f81458e85316cf63fe6b9ec70aeb9c8f2c5af0c74d3db8dd0d027a318f17f52a0f2e52455aed37dee9ffe4d5a1c714210f6e62800713eb4328d62f54f3ef2277ab848601a6a1c4e0ee7c7dcf613917da2fe4094cc5cdca51bdbb016add212cbdc26d56e90cb7358a6491a6289f0c84edbc4627158c3834a848699b68dfc6a36da12cc639d9999b6849bb84ec47a1aea412d7bff4e746d1d13d598ed0735b748fe47ad203f503b74df45f1c59a156c16ab02a74c9c5d342a706a43bbc787f58f5e011ab755f03d05475350f871570e7599446ea9df63625c56aec81e22ef7fce47a8b21fb93094dcc1322f19e4e7a6955315b39570b685262b042c0ab88fdb1cc20c64d26035b33020dbdc8a28cddc91e349a746bbec7a9c15871612cb2d3f077af9cbe01dd41d5b09e2b31ee3a849c35c1ad3de18d4edcce7347162f280972f0fa6f0d34a4e4f503c687787cb573754d82552e7574b46c4fb7fb6461e81ec2c97ed9004d810a2284180d9fec451435d767391c2cab70f372d10afad21b8c0a3ebb9c464a5dcc5e87355e4fe7fce395fdefcb4bae40d3108b6bb8fef305c89a04f8f829d487fedcc26f54a70734434150fa6d30ca04bfdc8abc09cd0b372a79c63f393efce8da1b18b22433b23564577b7949cb1e99c4f282201ccd36a2989b17237f20319e983e02079e93faf749dcc8a8709959cadc94cdd90f36c36f5f8c826dc55246b7c428b5b2568ccc47e7190706e8d1777c86e81dbd08dad98a7e422646ba774daf802f35f2175868e776ef95896909e6a1c5158751945788909923509c3440dd1c2849"
    # d = aes.decrypt(e)  # 调用解密函数
    # print(e)
    # print(d)
