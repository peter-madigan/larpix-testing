from django.db import models, transaction
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.sites.models import Site
from django.utils.html import format_html
from django.conf import settings
from django.core.files.base import ContentFile

import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO

status_key_list = [
    ('P', 'Pass'),
    ('F', 'Fail'),
    ('W', 'Weird'),
    ('M', 'Mixed'),
    ('U', 'Unknown')
    ]

def test_status_logic(prev_key, new_key):
    '''
    Return the new status assuming a previous status of `prev_key` and an
    additional status of `new_key`
    '''
    if new_key in ('F','U'):
        return new_key
    elif prev_key in (new_key):
        return prev_key
    elif prev_key in ('P', 'U'):
        return new_key
    elif prev_key in ('F', 'W'):
        return prev_key
    elif prev_key in ('M'):
        if new_key in ('P'):
            return 'M'
        elif new_key in ('W'):
            return 'W'
    else:
        return 'U'

qrcode_font = '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf'
def generate_qrcode(obj):
    '''
    Generates a qr code linking to admin modify url
    Obj must have version and id fields
    '''
    app_label = obj._meta.app_label
    model_name = obj._meta.model_name
    pk = obj.pk
    if not obj.pk:
        return None
    #data = 'https://' + str(Site.objects.get_current()) + reverse('admin:{0}_{1}_change'.format(app_label, model_name), args=(pk,))
    # data = reverse('{0}:{1}-detail'.format(app_label, model_name), args=(pk,))
    data = '{}/{}/{}'.format(app_label, model_name, pk)

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(back_color='transparent', fill_color='black')
    img_width, img_height = img.size
    draw = ImageDraw.Draw(img)

    img_text = '{}{:08d}'.format(model_name, pk).replace(' ','').upper()
    fontsize = 1
    font = ImageFont.truetype(qrcode_font, fontsize)
    text_width, text_height = draw.textsize(img_text, font=font)
    while text_width < img_width*0.8 and text_height < img_height*0.8 and \
        fontsize < 48:
        fontsize += 1
        font = ImageFont.truetype(qrcode_font, fontsize)
        text_width, text_height = draw.textsize(img_text, font=font)
    font = ImageFont.truetype(qrcode_font, fontsize)
    text_width, text_height = draw.textsize(img_text, font=font)

    text_img = Image.new("RGBA", (img_width, img_height), (0,0,0,0))
    text_draw = ImageDraw.Draw(text_img)
    text_draw.text((img_width*0.1, img_height*0.9), img_text, font=font, fill=(18,74,143))
    text_img90 = text_img.rotate(90)
    text_img180 = text_img.rotate(180)
    text_img270 = text_img.rotate(270)
    img.paste(text_img, mask=text_img)
    img.paste(text_img90, mask=text_img90)
    img.paste(text_img180, mask=text_img180)
    img.paste(text_img270, mask=text_img270)

    return img

class LArPixDBObject(models.Model):
    '''
    Base class for database entries
    '''
    entry_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        string = '{}('
        #string += 'entry_date={entry_date}, '
        string += ')'
        return string.format(type(self).__name__, **vars(self))

class LArPixDBObject_with_note(models.Model):
    '''
    database entries that have an option to add additional info
    '''
    note = models.TextField(blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        string = super().__str__()[:-1]
        string += 'modification_date={modification_date}'
        string += ')'
        return string.format(**vars(self))

class LArPixDBObject_with_qrcode(models.Model):
    '''
    database entries that have a qrcode associated with them
    '''
    qrcode = models.ImageField(upload_to='qrcodes/', null=True, blank=True)

    class Meta:
        abstract = True

    def qrcode_tag(self):
        url = self.qrcode.url
        return format_html('<img src="{}" width=150>'.format(url))
    qrcode_tag.short_description = 'QRCode'
    qrcode_tag.allow_tags = True

    def save(self, *args, **kwargs):
        '''
        Generate qr code on save
        '''
        super(LArPixDBObject_with_qrcode, self).save(*args, **kwargs)
        if not self.qrcode or not os.path.exists(self.qrcode.path):
            qrcode_img = generate_qrcode(self)
            qrcode_img_name = '{}{:08d}.png'.format(self._meta.model_name, self.id)
            qrcode_io = BytesIO()
            qrcode_img.save(qrcode_io, format='png')
            self.qrcode.save(
                os.path.basename(qrcode_img_name),
                content=ContentFile(qrcode_io.getvalue()),
                save=False
            )
            if 'force_insert' in kwargs:
                kwargs['force_insert'] = False
            super(LArPixDBObject_with_qrcode, self).save(*args, force_update=True, **kwargs)

class ASIC(LArPixDBObject, LArPixDBObject_with_note, LArPixDBObject_with_qrcode):
    '''
    Base class for LArPix ASICs
    '''
    _avail_versions = [
        ('1','LArPix v1'),
        ('2','LArPix v2')
        ]
    version = models.CharField(max_length=100, choices=_avail_versions)
    packaged = models.BooleanField(default=False)
    status = models.CharField(max_length=100, choices=status_key_list, default='U')

    class Meta:
        verbose_name_plural = 'ASICs'
        verbose_name = 'ASIC'

    def __str__(self):
        string = 'ASIC('
        string += '{id}, '
        string += 'version={version}, '
        string += 'packaged={packaged}, '
        string += 'status={status}'
        string += ')'
        return string.format(**vars(self))

class PCB(LArPixDBObject, LArPixDBObject_with_note, LArPixDBObject_with_qrcode):
    '''
    Base class for test boards
    '''
    _avail_versions = [
        ('1.1','4-chip pixelless test anode'),
        ('1.3','4-chip HPATS anode'),
        ('1.4','28-chip HPATS anode'),
        ('1.5', '4-chip packaged chip test anode')
        ]
    version = models.CharField(max_length=100, choices=_avail_versions)
    status = models.CharField(max_length=100, choices=status_key_list, default='U')

    class Meta:
        verbose_name_plural = 'PCBs'
        verbose_name = 'PCB'

    def __str__(self):
        string = 'PCB('
        string += '{id}, '
        string += 'version={version}, '
        string += 'status={status}'
        string += ')'
        return string.format(**vars(self))

class TestResult(LArPixDBObject, LArPixDBObject_with_note):
    '''
    Base class for test results
    '''
    _avail_versions = [
        ('noise-test-v1','Standard noise test (ADC RMS with low threshold)'),
        ('leakage-test-v1','Standard leakage test'),
        ('sensitivity-test-v1','Standard sensitivity test (configured to <1Hz/channel noise rate)')
        ]
    version = models.CharField(max_length=100, choices=_avail_versions)
    status = models.CharField(max_length=100, choices=status_key_list)
    asics = models.ManyToManyField('ASIC', blank=True, related_name='test_results', null=True)
    pcbs = models.ManyToManyField('PCB', blank=True, related_name='test_results', null=True)

    log = models.FileField('log', upload_to='test_logs/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Test results'
        verbose_name = 'Test result'

    def __str__(self):
        string = super().__str__()[:-1]
        #string += ', '
        string += '{id}, '
        string += 'version={version}, '
        string += 'status={status}'
        string += ')'
        return string.format(**vars(self))

    def save(self, *args, **kwargs):
        '''
        Make sure that statuses are propogated to associated objects
        '''
        super(TestResult, self).save(*args, **kwargs)
        transaction.on_commit(lambda: self.propogate_status())

    def propogate_status(self):
        '''
        Propogate test status to associated objects
        Propogation only goes in one direction ASIC -> PCB, i.e. a failed PCB
        does not imply a failed ASIC, but a failed ASIC implies a failed PCB
        '''
        updated_models = []
        # update asic statuses
        for asic in self.asics.all():
            if asic in updated_models: continue
            print(asic)
            asic.status = test_status_logic(asic.status, self.status)
            # update any pcbs connected to asics
            try:
                if not asic.connection.pcb in updated_models:
                    print(asic.connection.pcb)
                    asic.connection.pcb.status = test_status_logic(asic.connection.pcb.status, self.status)
                    asic.connection.pcb.save()
                    updated_models += [asic.connection.pcb]
            except Connection.DoesNotExist:
                pass
            finally:
                asic.save()
                updated_models += [asic]

        # update pcb statuses
        for pcb in self.pcbs.all():
            if pcb in updated_models: continue
            print(pcb)
            pcb.status = test_status_logic(pcb.status, self.status)
            pcb.save()

class LogbookEntry(LArPixDBObject):
    '''
    Base class for logbook entries
    '''
    _avail_types = [
        ('test','Test')
    ]
    _avail_versions = [
        ('0.0','v0.0')
    ]
    type = models.CharField(max_length=100, choices=_avail_types)
    version = models.CharField(max_length=100, choices=_avail_versions, default='0.0')
    title = models.CharField(max_length=100)
    entry = models.TextField(blank=True)
    associated_test_results = models.ManyToManyField('TestResult', blank=True, related_name='logbook_entries', null=True)
    associated_asics = models.ManyToManyField('ASIC', blank=True, related_name='logbook_entries', null=True)
    associated_pcbs = models.ManyToManyField('PCB', blank=True, related_name='logbook_entries', null=True)

    class Meta:
        verbose_name_plural = 'Logbook entries'
        verbose_name = 'Logbook entry'

    def __str__(self):
        string = 'LogbookEntry('
        string += '{id}, '
        string += 'entry_date={entry_date}, '
        string += 'modification_date={modification_date}'
        string += ')'
        return string.format(**vars(self))

class Connection(LArPixDBObject):
    '''
    Model for creating assiociations between chips and PCBs
    '''
    position_id = models.IntegerField(null=True)

    pcb = models.ForeignKey('PCB', on_delete=models.CASCADE, related_name='connections')
    asic = models.OneToOneField('ASIC', on_delete=models.CASCADE, related_name='connection')

    def __str__(self):
        string = 'Connection('
        string += 'pcb={pcb_id}, '
        string += 'asic={asic_id}, '
        string += 'position_id={position_id}'
        string += ')'
        return string.format(**vars(self))
