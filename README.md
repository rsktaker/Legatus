# Legatus

Personal API endpoint to process write and read requests to message bins - perfect for (indirect) communication between computers.


## Origins

At my university, the Intro CS class utilizes a code editor called Vocareum for editing/submitting HWs and Exams. Below is an example assignment:

<img width="700" alt="rsk1" src="https://github.com/user-attachments/assets/cc6d95b8-94b9-4091-92ec-1e083c1bf26d">


Exploring the Vocareum terminal, I found there were no restrictions on curl commands. I ran a simple api call to ChatGPT and confirmed that students could access AI generated code during exams from the editor's terminal itself:

<img width="700" alt="rsk2" src="https://github.com/user-attachments/assets/5258e50c-136d-4e08-b39a-c1bed74ad18c">


But that's quite the command to memorize (imagine writing _that_ on your hand or the inside of your shirt).

I wanted something your average student could easily use, so I had the idea to set up my computer as an messaging endpoint to enable communication between students during exams. Here is the basic functionality:

- Students can create a message bin and write messages to it with POST requests:
<img width="834" alt="rsk3" src="https://github.com/user-attachments/assets/f78557ae-fd13-478b-8a69-4ff489872d94">

- Students can read chat logs for a message bin with GET requests:
<img width="836" alt="rsk4" src="https://github.com/user-attachments/assets/e56b7db2-a2e0-46e3-9fec-68e3de6ae758">

- Students can list all active message bins with a GET request:
<img width="841" alt="rsk5" src="https://github.com/user-attachments/assets/5516b4e5-34c0-4f68-89ca-20ca45048989">



## Notice
This system was developed to **demonstrate** the potential for cheating and was never exploited for those purposes. All code was tested on the HW 1 assignment (which was already submitted) and **never** on an exam. 

Additionally, my professor & Vocareum were notified of this flaw before its public release and, to mitigate the issue, Vocareum is disabling network access from code editor terminals + updating their systems.


## Admin Implementation

Clone github repo (set admin_password & admin_name in .env) and run simple_server.py.

```bash
python3 simple_server.py
```

Sign up for ngrok (port forwarding) [here](https://dashboard.ngrok.com/signup) and get authtoken (free), configure ngrok
```bash
ngrok config add-authtoken <authtoken>
```
Portforwarding to port 8080. The 'Forwarding' link is essentially the url you use to make the curl commands.
```bash
ngrok http 8080
```
Run `curl $LINK` to check the list of all commands + copy/paste templates. Where LINK is ^ forwarding link.

## The Exotic Option

Wherever this server that's running my code is, nothing on it has been updated since 2016 so it matches the criteria for many known vulnerabilities.

For example, CVE-2019-0211 is a local privilege escalation that could potentially allow students to find and copy the solution code for an assignment (it must be stored somewhere...)


## License

[MIT](https://choosealicense.com/licenses/mit/)
