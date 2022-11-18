import sys, getopt
import requests
import dicttoxml
import json
import datetime
from xml.dom import minidom

baseurl = 'http://dynamicraceodds.com/xml/data/'
modeDic = [
            'GetMeetingsAll', 'GetMeeting', 'GetEvent', 'GetEventSchedule',
            'GetRunnersAll', 'GetRunnersMeeting', 'GetRunnersEvent',
            'GetBettingAgencies', 'GetRunnerOdds', 'GetEventResults',
            'GetExotics', 'GetBookmakerFlucs'
            ]


def getOfficalPrice(pm_timestamp):
    if pm_timestamp != '' or pm_timestamp != '0000000000':
        url = 'http://feeds.officialprice.com.au/feeds/op_feed_new.php?ts='+pm_timestamp
    else:
        url = 'http://feeds.officialprice.com.au/feeds/op_feed_new.php'
    try:
        r = requests.get(url)
        if r.status_code == 200:
            content = r.content.decode("utf-8")
            obj = json.loads(content)
            newobj = {}
            if 'event' in obj:
                newobj['event'] = []
                for x in obj['event']:
                    newobj['event'].append({'Event':x})
            for x in obj:
                if x != 'event':
                    newobj[x] = obj[x]
            xml = dicttoxml.dicttoxml(newobj, attr_type = False)
            xml = xml.decode("utf-8")
            xml = xml.replace("<item><Event>", "<Event>")
            xml = xml.replace("</Event></item>", "</Event>")
            xml = xml.replace("<item>", "<Runner>")
            xml = xml.replace("</item>", "</Runner>")
            xml = xml.replace("<weather/>", "")
            xml = xml.replace("<weather></weather>", "")
            xml = xml.replace("<price_flucs/>", "")
            xml = xml.replace("<price_flucs></price_flucs>", "")
            xml = xml.replace("<updated_ts/>", "<updated_ts xsi:nil=\"true\" />")
            return xml
    except:
        tmp = {'error':'no data'}
        txml = dicttoxml.dicttoxml(tmp, attr_type = False)
        return txml
    return ''

def getSession(pm_uid, pm_pwd):
    if len(pm_uid) != 26:
        print('Invalid clientid')
        sys.exit(2)
    if len(pm_pwd) != 52:
        print('Invalid clientsecuritykey')
        sys.exit(2)
    headers = {
        'cache-control':'no-cache',
        'content-type':'application/x-www-form-urlencoded'
    }
    params = {
        'grant_type':'client_credentials',
        'scope':'graphql/api',
        'client_id':pm_uid,
        'client_secret':pm_pwd
    }
    r = requests.post('https://bmcoredb-uat.auth.ap-southeast-2.amazoncognito.com/oauth2/token', headers=headers, params=params, data={})
    if r.status_code != 200:
        print('Invalid clientid')
        sys.exit(2)
    # userid = 'EricPhillips'
    # password = 'Roger4870'
    # url = "{baseurl}Login.asp?UserName={uid}&Password={pwd}".format(baseurl=baseurl, uid=userid, pwd=password)
    url = "http://ox21.xyz/oddsdb"
    r = requests.get(url)
    if r.status_code == 200:
        content = r.content.decode("utf-8")
        return content
    return ''

def getMeetingAll(pm_sessionid, pm_date_str, pm_type, pm_runner):
    if(pm_type == ''):
        pm_type = 'R,H,G'
    if(pm_runner == ''):
        pm_runner = 'true'
    url = "{baseurl}GetData.asp?SessionID={sid}&Method=GetMeetingsAll&Date={dt}&Types={tp}&Runners={rmode}".format(baseurl=baseurl, sid=pm_sessionid, dt=pm_date_str, tp=pm_type, rmode=pm_runner)
    try:
        r = requests.get(url)
        if r.status_code == 200:
            content = r.content.decode("utf-8")
            return content
    except requests.exceptions.ConnectionError as e:
        tmp = {'error':'no data'}
        txml = dicttoxml.dicttoxml(tmp, attr_type = False)
        return txml
    return ''

def getMeeting(pm_sessionid, pm_meetid, pm_runner):
    if(pm_runner == ''):
        pm_runner = 'true'
    url = "{baseurl}GetData.asp?SessionID={sid}&Method=GetMeeting&MeetingID={mt_id}&Runners={rmode}".format(baseurl=baseurl, sid=pm_sessionid, mt_id=pm_meetid, rmode=pm_runner)
    try:
        r = requests.get(url)
        if r.status_code == 200:
            content = r.content.decode("utf-8")
            return content
    except requests.exceptions.ConnectionError as e:
        tmp = {'error':'no data'}
        txml = dicttoxml.dicttoxml(tmp, attr_type = False)
        return txml
    return ''

def getEvent(pm_sessionid, pm_evtid, pm_runner):
    if(pm_runner == ''):
        pm_runner = 'true'
    url = "{baseurl}GetData.asp?SessionID={sid}&Method=GetEvent&EventID={evt_id}&Runners={rmode}".format(baseurl=baseurl, sid=pm_sessionid, evt_id=pm_evtid, rmode=pm_runner)
    try:
        r = requests.get(url)
        if r.status_code == 200:
            content = r.content.decode("utf-8")
            return content
    except requests.exceptions.ConnectionError as e:
        tmp = {'error':'no data'}
        txml = dicttoxml.dicttoxml(tmp, attr_type = False)
        return txml
    return ''

def getEventSchedule(pm_sessionid, pm_date_str, pm_type, pm_limit):
    if(pm_type == ''):
        pm_type = 'R,H,G'
    url = "{baseurl}GetData.asp?SessionID={sid}&Method=GetEventSchedule&Date={dt}&Types={tp}&Limit={lmt}".format(baseurl=baseurl, sid=pm_sessionid, dt=pm_date_str, tp=pm_type, lmt=pm_limit)
    try:
        r = requests.get(url)
        if r.status_code == 200:
            content = r.content.decode("utf-8")
            return content
    except requests.exceptions.ConnectionError as e:
        tmp = {'error':'no data'}
        txml = dicttoxml.dicttoxml(tmp, attr_type = False)
        return txml
    return ''

def getRunnersAll(pm_sessionid, pm_date_str, pm_type):
    if(pm_type == ''):
        pm_type = 'R,H,G'
    url = "{baseurl}GetData.asp?SessionID={sid}&Method=GetRunnersAll&Date={dt}&Types={tp}".format(baseurl=baseurl, sid=pm_sessionid, dt=pm_date_str, tp=pm_type)
    try:
        r = requests.get(url)
        if r.status_code == 200:
            content = r.content.decode("utf-8")
            return content
    except requests.exceptions.ConnectionError as e:
        tmp = {'error':'no data'}
        txml = dicttoxml.dicttoxml(tmp, attr_type = False)
        return txml
    return ''

def getRunnersMeeting(pm_sessionid, pm_meetid):
    url = "{baseurl}GetData.asp?SessionID={sid}&Method=GetRunnersMeeting&MeetingID={mt_id}".format(baseurl=baseurl, sid=pm_sessionid, mt_id=pm_meetid)
    try:
        r = requests.get(url)
        if r.status_code == 200:
            content = r.content.decode("utf-8")
            return content
    except requests.exceptions.ConnectionError as e:
        tmp = {'error':'no data'}
        txml = dicttoxml.dicttoxml(tmp, attr_type = False)
        return txml
    return ''

def getRunnersEvent(pm_sessionid, pm_evtid):
    url = "{baseurl}GetData.asp?SessionID={sid}&Method=GetRunnersEvent&EventID={evt_id}".format(baseurl=baseurl, sid=pm_sessionid, evt_id=pm_evtid)
    try:
        r = requests.get(url)
        if r.status_code == 200:
            content = r.content.decode("utf-8")
            return content
    except requests.exceptions.ConnectionError as e:
        tmp = {'error':'no data'}
        txml = dicttoxml.dicttoxml(tmp, attr_type = False)
        return txml
    return ''

def getBettingAgency(pm_sessionid):
    url = "{baseurl}GetData.asp?SessionID={sid}&Method=GetBettingAgencies".format(baseurl=baseurl, sid=pm_sessionid)
    try:
        r = requests.get(url)
        if r.status_code == 200:
            content = r.content.decode("utf-8")
            return content
    except requests.exceptions.ConnectionError as e:
        tmp = {'error':'no data'}
        txml = dicttoxml.dicttoxml(tmp, attr_type = False)
        return txml
    return ''

def getRunnerOdds(pm_sessionid, pm_eventid):
    url = "{baseurl}GetData.asp?SessionID={sid}&Method=GetRunnerOdds&EventID={evtid}".format(baseurl=baseurl, sid=pm_sessionid, evtid=pm_eventid)
    try:
        r = requests.get(url)
        if r.status_code == 200:
            content = r.content.decode("utf-8")
            return content
    except requests.exceptions.ConnectionError as e:
        tmp = {'error':'no data'}
        txml = dicttoxml.dicttoxml(tmp, attr_type = False)
        return txml
    return ''

def getEventResults(pm_sessionid, pm_eventid):
    url = "{baseurl}GetData.asp?SessionID={sid}&Method=GetEventResults&EventID={evtid}".format(baseurl=baseurl, sid=pm_sessionid, evtid=pm_eventid)
    try:
        r = requests.get(url)
        if r.status_code == 200:
            content = r.content.decode("utf-8")
            return content
    except requests.exceptions.ConnectionError as e:
        tmp = {'error':'no data'}
        txml = dicttoxml.dicttoxml(tmp, attr_type = False)
        return txml
    return ''

def getExotics(pm_sessionid, pm_eventid):
    url = "{baseurl}GetData.asp?SessionID={sid}&Method=GetExotics&EventID={evtid}&ExoticType=QQ".format(baseurl=baseurl, sid=pm_sessionid, evtid=pm_eventid)
    try:
        r = requests.get(url)
        if r.status_code == 200:
            content = r.content.decode("utf-8")
            return content
    except requests.exceptions.ConnectionError as e:
        tmp = {'error':'no data'}
        txml = dicttoxml.dicttoxml(tmp, attr_type = False)
        return txml
    return ''

def getBookmakerFlucs(pm_sessionid, pm_eventid):
    url = "{baseurl}GetData.asp?SessionID={sid}&Method=GetBookmakerFlucs&EventID={evtid}&BAID=baid".format(baseurl=baseurl, sid=pm_sessionid, evtid=pm_eventid)
    try:
        r = requests.get(url)
        if r.status_code == 200:
            content = r.content.decode("utf-8")
            return content
    except requests.exceptions.ConnectionError as e:
        tmp = {'error':'no data'}
        txml = dicttoxml.dicttoxml(tmp, attr_type = False)
        return txml
    return ''

def writeXml(str, path, hasMode):
    if type(str) == bytes:
        str = str.decode("utf-8")
    if hasMode:
        f = open(path, "w", encoding="utf-8")
        f.write(str)
    else:
        xmlstr = minidom.parseString(str).toprettyxml(indent="   ")
        with open(path, "w") as f:
            f.write(xmlstr)
    f.close()

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"t:m:u:p:s:d:e:f:l:r:",[])
    except getopt.GetoptError:
        print('Invalid command')
        sys.exit(2)
    hasMode = False
    mode = ''
    timestamp = ''
    userid = ''
    password = ''
    sessionid = ''
    datestr = ''
    eventid = ''
    fileout = ''
    limit = ''
    runners = ''
    for opt, arg in opts:
        if arg[0] == '=':
            arg = arg[1:]
        if opt == '-m':
            hasMode = True
            mode = arg
        elif opt == '-t':
            timestamp = arg
        elif opt == '-u':
            userid = arg
        elif opt == '-p':
            password = arg
        elif opt == '-s':
            sessionid = arg
        elif opt == '-d':
            datestr = arg
        elif opt == '-e':
            eventid = arg
        elif opt == '-f':
            fileout = arg
        elif opt == '-l':
            limit = arg
        elif opt == '-r':
            runners = arg
    content = ''
    if hasMode or not hasMode and timestamp != '':
        if fileout == '':
            print('Please input xml file path')
            sys.exit(2)
        if not hasMode:
            content = getOfficalPrice(timestamp)
        else:
            if mode == 'Login':
                content = getSession(userid, password)
            elif mode in modeDic:
                if sessionid == '':
                    print('Please input xml sessionid')
                    sys.exit(2)
                if mode == 'GetMeetingsAll':
                    content = getMeetingAll(sessionid, datestr, timestamp, runners)
                if mode == 'GetMeeting':
                    content = getMeeting(sessionid, eventid, runners)
                if mode == 'GetEvent':
                    content = getEvent(sessionid, eventid, runners)
                if mode == 'GetEventSchedule':
                    content = getEventSchedule(sessionid, datestr, timestamp, limit)
                
                if mode =='GetRunnersAll':
                    content = getRunnersAll(sessionid, datestr, timestamp)
                if mode =='GetRunnersMeeting':
                    content = getRunnersMeeting(sessionid, eventid)
                if mode =='GetRunnersEvent':
                    content = getRunnersEvent(sessionid, eventid)

                if mode == 'GetBettingAgencies':
                    content = getBettingAgency(sessionid)
                if mode == 'GetRunnerOdds':
                    content = getRunnerOdds(sessionid, eventid)
                if mode == 'GetEventResults':
                    content = getEventResults(sessionid, eventid)
                
                if mode == 'GetExotics':
                    content = getExotics(sessionid, eventid)
                if mode == 'GetBookmakerFlucs':
                    content = getBookmakerFlucs(sessionid, eventid)
    else:
        print('Invalid command')
        sys.exit(2)
    
    if content != '':
        writeXml(content, fileout, hasMode)
    else:
        print('Network connection error')
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])