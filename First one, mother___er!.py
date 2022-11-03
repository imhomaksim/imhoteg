import logging
from telethon.tl.types import Message
from .. import loader, utils

# meta developer: @minimaxno
# meta pic: https://img.icons8.com/emoji/344/bullseye.png

def getnum(list: list, needle: str) -> int:
    for i in range(0, len(list)):
        if list[i] == needle:
            return i

@loader.tds
class FirstOneMFMod(loader.Module):
    """Autocommenting."""
    strings = {
        'name': 'First one, mother***er!',
        'on': '⬆️ <b>FOMF-mode for channel turned on.</b>',
        'off': '⬇️ <b>FOMF-mode for channel turned off.</b>',
        'args?': '😕 <b>Ass ate args?</b>',
        'ans?': '😡 <b>Must be an answer to channel or comment.</b>'}
    strings_ru = {
        'name': 'First one, mother***er!',
        'on': '⬆️ <b>Первонах включен.</b>',
        'off': '⬇️ <b>Первонах выключен.</b>',
        'args?': '😕 <b>Жопа съела аргументы?</b>',
        'ans?': '😡 <b>Должно быть ответом на автосообщение канала или комментом.</b>'
    }
    
    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        if not self.get('fomf', False):
            self.set('fomf', {})
            
    async def fomfcmd(self, m: Message):
        """Configures FOMF in this chat."""
        if not hasattr(m, 'reply_to'):
            return utils.answer(m, self.strings(m, 'ans?'))
        r = await m.get_reply_message()
        if r is None:
            return utils.answer(m, self.strings(m, 'ans?'))
        if not hasattr(r.peer_id, 'channel_id'):
            return await utils.answer(m, self.strings(m, 'ans?'))
        try:
            if (utils.get_args_raw(m) == '') and (str(utils.get_chat_id(m)) not in self.get('fomf').keys()):
                return await utils.answer(m, self.strings('args?'))
        except:
            return await utils.answer(m, self.strings('args?'))
        if (str(utils.get_chat_id(m)) not in self.get('fomf').keys()) or utils.get_args_raw(m) != '':
            fomf = self.get('fomf')
            tt = m.text.split(" ", 1)[1]
            text = tt
            filtr = ''
            if ' ※ ' in tt:
                text, filtr = tt.split(' ※ ', 1)
            if filtr == '':
                fomf.update({str(utils.get_chat_id(m)): f'{str(r.from_id)}; {text}'})
            else:
                fomf.update({str(utils.get_chat_id(m)): f'{str(r.from_id)}; {text} ※ {filtr}'})
            self.set('fomf', fomf)
            await utils.answer(m, self.strings('on'))
        else:
            fomf = self.get('fomf')
            del fomf[str(utils.get_chat_id(m))]
            self.set('fomf', fomf)
            await utils.answer(m, self.strings('off'))
            
    async def watcher(self, m: Message):
            if not hasattr(m, 'out'):
                return
            if str(utils.get_chat_id(m)) not in self.get('fomf').keys():
                return
            if not hasattr(m, 'peer_id'):
                return
            if not hasattr(m.peer_id, 'channel_id'):
                return
            trigger = self.get('fomf')[str(utils.get_chat_id(m))].split('; ', 1)[1]
            if self.get('fomf')[str(utils.get_chat_id(m))].split('; ', 1)[0] != str(m.from_id):
                return
            if ' ※ ' in trigger:
                if trigger.split(' ※ ')[1] not in m.text:
                    return
                else:
                    return await m.reply(trigger.split(' ※ ')[0])
            await m.reply(self.get('fomf')[str(utils.get_chat_id(m))].split('; ', 1)[1])
            