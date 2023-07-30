from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required
import qrcode
import qrcode.image.svg
from django.conf import settings
import pandas as pd
import re
from django.template import Template, Context
from django.core.mail import EmailMessage, EmailMultiAlternatives
from .forms import *
from django.contrib import messages
from django.http import HttpResponse, FileResponse , Http404



def registratie(request,uidb64,eve):
    form = ContactForm()
    eves = force_str(urlsafe_base64_decode(eve))
    emailc = force_str(urlsafe_base64_decode(uidb64))
    context = {'form':form,'email':emailc, 'eves': eves}
    if Bezoeker.objects.filter(email=emailc).exists() is False or Bezoeker.objects.filter(evenements=eves).exists() is True and Bezoeker.objects.filter(evenements=eves).exists()  is False:
        
   

        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                factory = qrcode.image.svg.SvgImage
                data = 'http://localhost:8000/check/' + uidb64
                img = qrcode.make(data)
                img_name = 'qr' + emailc + '.png'
            
    
                img.save('static' + '/' + img_name)

            # Hier wordt het toegangsticket naar de klanten verstuurd,  de html template en mail subject mag altijd aangepast worden het protocol en domain NIET (anders is code kapot :-/ )
            gast = Bezoeker(fname = request.POST['fname'], lname = request.POST['lname'], email = emailc, functie = request.POST['functie'], aanwezigheid = 0, evenements = eves)
            gast.save()
            mail_subject = 'Toegangsticket'
            html_message = render_to_string('mail2.html', {
                   'img_name' : img_name,
                    'user': form.cleaned_data.get('fname'),
                    'domain': get_current_site(request).domain,
                    'protocol': 'https' if request.is_secure() else 'http' 
            })
            email = EmailMultiAlternatives(mail_subject, html_message, bcc=[emailc])
            email.attach_file('static' + '/' + img_name)
            email.attach_alternative(html_message, 'text/html')
            email.send()
            #Hier wordt een QR code gegenereerd die uniek is voor de gebruiker (gebasseerd op email adress uit mailinglijst) De verwerking van de QR code gebeurt NIET in deze funcitie
            return redirect('merci')
    else:
        return redirect('merci')
    
    return render(request, 'registratie.html',context)

   








def merci(request):
    return render(request, 'merci.html')








@login_required(login_url = 'admin:index')

def mailsturen(request,pk):
    eve = evenement.objects.get(id=pk)



    q = eve.maillijst.name.split(".")[-1]
    lines = []
    if q == 'txt':
        file = eve.maillijst.open('r')
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        file.close()
        
    elif q == '.xls' or q == 'xlsx' :
        df = pd.read_excel(eve.maillijst)
        lines = df.values.tolist()
        lines = [item for sublist in lines for item in sublist]
    
    slist = []

    mail_subject = eve.onderwerpmail
    for i in lines:
        slist.append(i)
        if re.match(r'^[\w\.-]+@gmail.com$', i, re.IGNORECASE):


            htemplate = eve.mailtemplate

            context = {
                'eve': urlsafe_base64_encode(force_bytes(eve.name)),
                'uid' : urlsafe_base64_encode(force_bytes(i)),
                'domain' : get_current_site(request).domain,
                'protocol': 'https' if request.is_secure() else 'http'
            }
            template = Template(htemplate)
            rendered_html = template.render(Context(context))

           

        else:

            htemplate = eve.mailtemplateoutlook

            context = {
                'eve': urlsafe_base64_encode(force_bytes(eve.name)),
                'uid' : urlsafe_base64_encode(force_bytes(i)),
                'domain' : get_current_site(request).domain,
                'protocol': 'https' if request.is_secure() else 'http'
            }
            template = Template(htemplate)
            rendered_html = template.render(Context(context))


            

        email = EmailMultiAlternatives(mail_subject, rendered_html ,bcc=slist)
        email.attach_alternative(rendered_html, 'text/html')
        email.send()
        slist.clear()
    
    return redirect('mailcentrum')








@login_required(login_url = 'admin:index')
def qrcodecheck(request,uidb64):
    emailid = force_str(urlsafe_base64_decode(uidb64))
    persoon  = Bezoeker.objects.get(email  = emailid)
    checkform = aanwezig(instance=persoon)

    if request.method == 'POST':
        checkform = aanwezig(request.POST ,instance=persoon)
        if checkform.is_valid():
            checkform.instance.aanwezigheid = 1
            checkform.save()
            return redirect('overzicht')
        
    context = {'check':checkform}
    return render(request, 'checkqr.html', context)



@login_required(login_url = 'admin:index')
def overzicht(request):
    eve = evenement.objects.all()
    personen = Bezoeker.objects.all()

    context = {'eve':eve, 'personen': personen,}
    return render(request, 'overzicht.html' ,context)




@login_required(login_url = 'admin:index')
def mailselector(request):
    eve = evenement.objects.all()
    context = {'eve':eve}
    return render(request, 'mailcentrum.html' , context)


@login_required(login_url = 'admin:index')
def send(request,pk):
    eve = evenement.objects.get(id=pk)
    q = eve.maillijst.name.split(".")[-1]
    lines = []
    if q == 'txt':
        file = eve.maillijst.open('r')
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        file.close()
        
    elif q == '.xls' or q == 'xlsx' :
        df = pd.read_excel(eve.maillijst)
        lines = df.values.tolist()
        lines = [item for sublist in lines for item in sublist]





    context = {'eve':eve, 'lines':lines}
    if request.method == 'POST':
        mailsturen()
    
    return render(request, 'emailsender.html', context)

def terms(request):
    return render(request, 'GDPR.html')


def evene(request,pk):
    eve = evenement.objects.get(id=pk)
    Bezoekers = Bezoeker.objects.all()

    ml = []
    for i in Bezoekers:
        if i.evenements  == eve.name and i.aanwezigheid ==0:
            ml.append(i.email)

    df = pd.DataFrame(ml, columns=['Email'])
    output_file_path = os.path.join(settings.MEDIA_ROOT, str(eve.id) + 'maillijst.xlsx')

    df.to_excel(output_file_path, index=False)

    q = eve.maillijst.name.split(".")[-1]
    lines = []
    if q == 'txt':
        file = eve.maillijst.open('r')
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        file.close()
        
    elif q == '.xls' or q == 'xlsx' :
        df = pd.read_excel(eve.maillijst)
        lines = df.values.tolist()
        lines = [item for sublist in lines for item in sublist]

    context = {'eve':eve, 'bezoeker':Bezoekers ,'lines':lines, 'download_url': '/download/'}
    return render(request, 'evenement.html', context)
    


def download_file(request,pk):
    eve = evenement.objects.get(id=pk)
    # Replace 'output.xlsx' with the actual filename and path of the file to be downloaded
    file_path = os.path.join(settings.MEDIA_ROOT, str(eve.id) + 'maillijst.xlsx')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = FileResponse(file)
            response['Content-Disposition'] = f'attachment; filenamestr(eve.id) + "output.xlsx" '
        return response
    else:
        # If the file doesn't exist, you can handle the case appropriately (e.g., show a 404 page)
            raise Http404("File not found")

#Reserve Code

# html_message = render_to_string( 'mail.html', {
            #     'eve': urlsafe_base64_encode(force_bytes(eve.name)),
            #     'uid' : urlsafe_base64_encode(force_bytes(i)),
            #     'domain' : get_current_site(request).domain,
            #     'protocol': 'https' if request.is_secure() else 'http'
            # })
