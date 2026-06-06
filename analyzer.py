import ntplib
import time

def patch_time():
    try:
        c = ntplib.NTPClient()
        r = c.request('pool.ntp.org', version=3)
        offset = r.offset
        original_time = time.time
        time.time = lambda: original_time() + offset
        print(f"⏱ Уақыт түзету: {int(offset * 1000)} мс")
    except Exception as e:
        print(f"⚠️ NTP қатесі: {e}")