import asyncio
import datetime as dt

from onvif_utilities.parser import PARSERS
from onvif_utilities.main_class import Camera
from onvif_utilities.eventException import ONVIFUtilitiesError

UNHANDLED_TOPICS = set()

class CameraEvent(Camera):

    async def start_polling(self):
        await self.camera.update_xaddrs()
        if await self.camera.create_pullpoint_subscription():
            pullpoint = self.camera.create_pullpoint_service()
            await pullpoint.SetSynchronizationPoint()
            req = pullpoint.create_type("PullMessages")
            req.MessageLimit = 50
            req.Timeout = dt.timedelta(seconds=5)
            response = await pullpoint.PullMessages(req)
            await self.parse_messages(response.NotificationMessage)

    async def parse_messages(self, messages):
        for msg in messages:
            if not msg.Topic:
                continue
            topic = msg.Topic._value_1
            parser = PARSERS.get(topic)
            if not parser:
                if topic not in UNHANDLED_TOPICS:
                    print("No registered handler for event.",)
                    UNHANDLED_TOPICS.add(topic)
                continue
            event = await parser(msg)

            if not event:
                print("Unable to parse event.")
                return
            return event
    
    async def get_snapshot(self):
        try:
            media_service_profile = await self.media_service.GetProfiles()        
            image = await self.camera.get_snapshot(media_service_profile[0].token)
            return image 
        except Exception as e:
            raise ONVIFUtilitiesError(
                str(e)
            )

if __name__=="__main__":
    async def run(): 
        ip_list = ['192.168.2.206', '192.168.2.207', '192.168.2.204', '192.168.2.231']
        for i in ip_list:
            a = CameraEvent(ip=i,
                port="80",
                username="admin", password="Sensifai")
            await a.get_snapshot()
        await a.camera.close()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())