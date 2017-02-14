title: "BSides San Francisco CTF 'Flag Receiver' writeup"
date: 2017-02-14 19:00
category: writeups
tags:

	- ctf
	- android
	- mobile
	- writeup
teaser:
	Writeup of Flag Receiver task from BSides San Francisco CTF 2017.
---

**Flag Receiver – 200*

*Here is a simple mobile application that will hand you the flag.. if you ask for it the right way.*

**P.S, it is meant to have a blank landing activity  Use string starting with Flag:* [flagstore.apk](flagstore.apk)

First of all, I decompiled apk code with [apktool](https://ibotpeaches.github.io/Apktool/) and [enjarify](https://github.com/google/enjarify):
```sh
➜  apktool d --no-src flagstore.apk
➜  enjarify flagstore/classes.dex -o classes.jar
```

Then I browsed application code using [JD-GUI](http://jd.benow.ca) and found that 

1. It registers [BroadcastReceiver](https://developer.android.com/reference/android/content/BroadcastReceiver.html) called `Send_to_Activity`  for `com.flagstore.ctf.INCOMING_INTENT` action:

```java
protected void onCreate(Bundle paramBundle)
{
    super.onCreate(paramBundle);
    TextView localTextView = new android/widget/TextView;
    Context localContext = getApplicationContext();
    localTextView.<init>(localContext);
    localTextView.setText("To-do: UI pending");
    setContentView(localTextView);
    IntentFilter localIntentFilter = new android/content/IntentFilter;
    localIntentFilter.<init>();
    localIntentFilter.addAction("com.flagstore.ctf.INCOMING_INTENT");
    Send_to_Activity localSend_to_Activity = new com/flagstore/ctf/flagstore/Send_to_Activity;
    localSend_to_Activity.<init>();
    registerReceiver(localSend_to_Activity, localIntentFilter, "ctf.permissions._MSG", null);
}
```

2. After receiving `com.flagstore.ctf.INCOMING_INTENT` it checks that `msg` parameter of this intent is equal to `OpenSesame` and if it is true the application starts new activity called `CTFReceiver`:

```java
public void onReceive(Context paramContext, Intent paramIntent)
{
    String str1 = paramIntent.getStringExtra("msg");
    Intent localIntent = null;
    Object localObject = "OpenSesame";
    int i = str1.equalsIgnoreCase((String)localObject);
    if (i != 0)
    {
      String str2 = "Intent";
      Log.d("Here", str2);
      localIntent = new android/content/Intent;
      localObject = CTFReceiver.class;
      localIntent.<init>(paramContext, (Class)localObject);
      paramContext.startActivity(localIntent);
    }
    for (;;)
    {
      return;
      String str3 = "Ah, ah, ah, you didn't say the magic word!";
      i = 1;
      localObject = Toast.makeText(paramContext, str3, i);
      ((Toast)localObject).show();
    }
}
```

3. Then in `CTFReceiver` activity in `OnClick` event handler it does weird things with some strings using the code from native library (libnative-lib.so) and broadcasts the result as `msg` parameter of `com.flagstore.ctf.OUTGOING_INTENT`:

```java
public void onClick(View paramView)
{
    Intent localIntent = new android/content/Intent;
    localIntent.<init>();
    localIntent.setAction("com.flagstore.ctf.OUTGOING_INTENT");
    StringBuilder localStringBuilder = new java/lang/StringBuilder;
    localStringBuilder.<init>();
    String str1 = this.this$0.getResources().getString(2131099686);
    String str2 = str1 + "fpcMpwfFurWGlWu`uDlUge";
    String str3 = Utilities.doBoth(this.this$0.getResources().getString(2131099683));
    String str4 = getClass().getName().split("\\.")[4];
    int i = str4.length() + -2;
    String str5 = Utilities.doBoth(str4.substring(0, i));
    String str6 = this.this$0.getPhrase(str2, str3, str5);
    localIntent.putExtra("msg", str6);
    this.this$0.sendBroadcast(localIntent);
}
```

So, to get flag we should:

1. Send `com.flagstore.ctf.INCOMING_INTENT` with parameter `msg="OpenSesame"` to the app.
2. Click the button in `CTFReciever` activity
3. Get `msg` parameter of `com.flagstore.ctf.INCOMING_INTENT`

I decieded to try something new, i.e. not to use debugger and solve this task by using android emulator, adb and tool called [drozer](https://github.com/mwrlabs/drozer). Let's start!

First of all,  run an android emulator and install flagstore.apk to it:

```sh
➜  emulator -avd 24_x86_64
➜  adb install flagstore.apk
```

Then, install drozer client and its dependencites to your computer:

```sh
➜  wget https://github.com/mwrlabs/drozer/releases/download/2.4.2/drozer-2.4.2-py2.7.egg
➜  easy_install drozer-2.4.2-py2.7.egg
➜  pip install twisted
```

After that, generate drozer agent apk and install it to the emulator:

```sh
➜  drozer agent build
...
Done: /var/folders/s4/hf3pw66928v6qdhftl_53lkr0000gn/T/tmpAKONaf/agent.apk
➜  adb install /var/folders/s4/hf3pw66928v6qdhftl_53lkr0000gn/T/tmpAKONaf/agent.apk
```

 Run drozer agent on the emulator and click the *On* button:

![](drozer.png)

On your computer forward drozer's port and connect to it using the client:

```sh
➜  adb forward tcp:31415 tcp:31415
➜  drozer console connect
Selecting 83e5e2881cdf4d59 (unknown Android SDK built for x86_64 7.0)

            ..                    ..:.
           ..o..                  .r..
            ..a..  . ....... .  ..nd
              ro..idsnemesisand..pr
              .otectorandroidsneme.
           .,sisandprotectorandroids+.
         ..nemesisandprotectorandroidsn:.
        .emesisandprotectorandroidsnemes..
      ..isandp,..,rotectorandro,..,idsnem.
      .isisandp..rotectorandroid..snemisis.
      ,andprotectorandroidsnemisisandprotec.
     .torandroidsnemesisandprotectorandroid.
     .snemisisandprotectorandroidsnemesisan:
     .dprotectorandroidsnemesisandprotector.

drozer Console (v2.4.2)
dz>
```

In drozer console start listening to`com.flagstore.ctf.OUTGOING_INTENT` action:

```sh
dz> run app.broadcast.sniff --action "com.flagstore.ctf.OUTGOING_INTENT"
[*] Broadcast receiver registered to sniff matching intents
[*] Output is updated once a second. Press Control+C to exit.
```

Then, run the flagstore application on the emulator:

![](flagstore.png)

 Send `com.flagstore.ctf.INCOMING_INTENT` with correct `msg` parameter to the app using adb:

```sh
➜  adb shell
generic_x86_64:/ $ su
generic_x86_64:/ $ am broadcast -a "com.flagstore.ctf.INCOMING_INTENT" --es msg "OpenSesame"
```

Click appeared *Broadcast* button in the emulator:

![](broadcast.png)

Finally, in dozer console you see:

```sh
Action: com.flagstore.ctf.OUTGOING_INTENT
Raw: Intent { act=com.flagstore.ctf.OUTGOING_INTENT flg=0x10 (has extras) }
Extra: msg=CongratsGoodWorkYouFoundItIHopeYouUsedADBFlag:TheseIntentsAreFunAndEasyToUse (java.lang.String)
```

