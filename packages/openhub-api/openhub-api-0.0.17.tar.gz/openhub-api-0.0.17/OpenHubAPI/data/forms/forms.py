from django import forms

from django.forms import ChoiceField

from data.models.models import Calibration, Hardware, Accessory, Channel, HardwareConfig, \
    CalibrationConstants, DHT22, MCP3008, \
    ModProbe, PiPico, VEML7700, HardwareChannelTypes, Hub, Category, AccessoryType, SPIIo, SerialIo, PwmIo, I2cIo, \
    DeviceFileIo, MCPAnalogIo, PiGpio, PiPicoAnalogIo, HardwareIO


class HubForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HubForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        categories = list(
            Category.objects.all().values_list('enum', 'name'))
        # categories = [('----', '-----')]
        # for chan_type in channel_types_temp:
        #     channel_types.append((chan_type['channel_type'], chan_type['channel_type']))

        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

        self.fields['category'] = ChoiceField(choices=tuple(categories))

    class Meta:
        model = Hub
        fields = ("__all__")


class CalibrationConstantForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CalibrationConstantForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap

        for name in self.fields.keys():
            if name == 'calibration':
                self.fields[name].widget = forms.HiddenInput()
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = CalibrationConstants
        fields = ("__all__")


class CalibrationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CalibrationForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            if name == 'accessory':
                self.fields[name].widget = forms.HiddenInput()
            else:
                self.fields[name].widget.attrs.update({
                    'class': 'form-control',
                })

    class Meta:
        model = Calibration
        fields = ("__all__")


class HardwareForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HardwareForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print('asdf')
        for name in self.fields.keys():
            if name == 'type':
                self.fields[name].widget = forms.HiddenInput()
            print(name)
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Hardware
        fields = ("__all__")


class HardwareDHT22Form(HardwareForm):
    def __init__(self, *args, **kwargs):
        super(HardwareDHT22Form, self).__init__(*args, **kwargs)

    class Meta:
        model = DHT22
        fields = ("__all__")


class HardwareMCP3008Form(HardwareForm):
    def __init__(self, *args, **kwargs):
        super(HardwareMCP3008Form, self).__init__(*args, **kwargs)

    class Meta:
        model = MCP3008
        fields = ("__all__")


class HardwareModProbeForm(HardwareForm):
    def __init__(self, *args, **kwargs):
        super(HardwareModProbeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ModProbe
        fields = ("__all__")


class HardwarePiPicoForm(HardwareForm):
    def __init__(self, *args, **kwargs):
        super(HardwarePiPicoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PiPico
        fields = ("__all__")


class HardwareVEML7700Form(HardwareForm):
    def __init__(self, *args, **kwargs):
        super(HardwareVEML7700Form, self).__init__(*args, **kwargs)

    class Meta:
        model = VEML7700
        fields = ("__all__")


class AccessoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AccessoryForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            # if name == 'channels':
            #     self.fields[name]= forms.ModelChoiceField(queryset=Channel.objects.all().values(('id')), empty_label="(Nothing)")
            # else:
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

        categories = list(
            Category.objects.all().values_list('enum', 'name'))
        self.fields['category'] = ChoiceField(choices=tuple(categories))

        types = list(
            AccessoryType.objects.all().values_list('type', 'type'))
        self.fields['type'] = ChoiceField(choices=tuple(types))

    class Meta:
        model = Accessory
        fields = ("__all__")


class ChannelForm(forms.ModelForm):

    def __init__(self, hardware_type=None, *args, **kwargs):
        super(ChannelForm, self).__init__(*args, **kwargs)
        if hardware_type is not None:
            channel_types_temp = list(
                HardwareChannelTypes.objects.filter(hardware_type=hardware_type).values('channel_type'))
            channel_types = [('----', '-----')]
            for chan_type in channel_types_temp:
                channel_types.append((chan_type['channel_type'], chan_type['channel_type']))
            self.fields['type'] = ChoiceField(choices=tuple(channel_types))

        # self.fields['type'] = ChoiceField(queryset=HardwareChannelTypes.objects.filter(hardware_type=hardware_type).values_list('channel_type'))
        # self.fields['type'].queryset = HardwareChannelTypes.objects.filter(hardware_type=hardware_type)

        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            if name == 'hardware':
                self.fields[name].widget = forms.HiddenInput()
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Channel
        fields = ("__all__")


class HardwareConfigForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HardwareConfigForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = HardwareConfig
        fields = ("__all__")


class HardwareIoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HardwareIoForm, self).__init__(*args, **kwargs)
        # self.fields['type'] = ChoiceField(choices=tuple(channel_types))

        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        # print('asdf')
        # for name in self.fields.keys():
        #     if name in ('parent_hardware', 'child_hardware', 'id', 'child_channel', 'hub'):
        #         self.fields[name].widget = forms.HiddenInput()
        #     print(name)
        #     self.fields[name].widget.attrs.update({
        #         'class': 'form-control',
        #     })
    class Meta:
        model = HardwareIO
        fields = ("__all__")

class SPIIoForm(HardwareIoForm):

    def __init__(self, *args, **kwargs):
        super(SPIIoForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print('asdf')
        for name in self.fields.keys():
            if name in ('parent_hardware', 'child_hardware', 'id', 'child_channel', 'hub'):
                self.fields[name].widget = forms.HiddenInput()
            print(name)
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = SPIIo
        fields = ("__all__")


class SerialIoForm(HardwareIoForm):

    def __init__(self, *args, **kwargs):
        super(SerialIoForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print('asdf')
        for name in self.fields.keys():
            if name in ('parent_hardware', 'child_hardware', 'id', 'child_channel', 'hub'):
                self.fields[name].widget = forms.HiddenInput()
            print(name)
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = SerialIo
        fields = ("__all__")


class PwmIoForm(HardwareIoForm):
    def __init__(self, *args, **kwargs):
        super(PwmIoForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print('asdf')
        for name in self.fields.keys():
            if name in ('parent_hardware', 'child_hardware', 'id', 'child_channel', 'hub'):
                self.fields[name].widget = forms.HiddenInput()
            print(name)
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = PwmIo
        fields = ("__all__")


class I2cIoForm(HardwareIoForm):

    def __init__(self, *args, **kwargs):
        super(I2cIoForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print('asdf')
        for name in self.fields.keys():
            if name in ('parent_hardware', 'child_hardware', 'id', 'child_channel', 'hub'):
                self.fields[name].widget = forms.HiddenInput()
            print(name)
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = I2cIo
        fields = ("__all__")


class DeviceFileIoForm(HardwareIoForm):

    def __init__(self, *args, **kwargs):
        super(DeviceFileIoForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print('asdf')
        for name in self.fields.keys():
            if name in ('parent_hardware', 'child_hardware', 'id', 'child_channel', 'hub'):
                self.fields[name].widget = forms.HiddenInput()
            print(name)
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = DeviceFileIo
        fields = ("__all__")


class MCPAnalogIoForm(HardwareIoForm):

    def __init__(self, *args, **kwargs):
        super(MCPAnalogIoForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print('asdf')
        for name in self.fields.keys():
            if name in ('parent_hardware', 'child_hardware', 'id', 'child_channel', 'hub'):
                self.fields[name].widget = forms.HiddenInput()
            print(name)
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = MCPAnalogIo
        fields = ("__all__")


class PiPicoAnalogIoForm(HardwareIoForm):

    def __init__(self, *args, **kwargs):
        super(PiPicoAnalogIoForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print('asdf')
        for name in self.fields.keys():
            if name in ('parent_hardware', 'child_hardware', 'id', 'child_channel', 'hub'):
                self.fields[name].widget = forms.HiddenInput()
            print(name)
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = PiPicoAnalogIo
        fields = ("__all__")


class PiGpioForm(HardwareIoForm):

    def __init__(self, *args, **kwargs):
        super(PiGpioForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        print('asdf')
        for name in self.fields.keys():
            if name in ('parent_hardware', 'child_hardware', 'id', 'child_channel', 'hub'):
                self.fields[name].widget = forms.HiddenInput()
            print(name)
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = PiGpio
        fields = ("__all__")


DHT22 = 'DHT22'
MCP3008 = 'MCP3008'
ModProbe = 'ModProbe'
PiPico = 'PiPico'
VEML7700 = 'VEML7700'
CHOICES = (('DHT22', 'DHT22'), ('MCP3008', 'MCP3008'), ('ModProbe', 'ModProbe'), ('PiPico', 'PiPico'),
           ('VEML7700', 'VEML7700'))


class HardwareTypeForm(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     super(HardwareTypeForm, self).__init__(*args, **kwargs)

    type = forms.ChoiceField(choices=CHOICES)


SPI = 'SPI'
Serial = 'Serial'
PWM = 'PWM'
I2C = 'I2C'
DeviceFile = 'Device File'
MCPChannel = 'MCP Channel'
PiPicoAnalog = 'Pi Pico Analog'
PiGPIO = 'Pi GPIO'

hardware_io_choices = (
    (SPI, SPI), (Serial, Serial), (PWM, PWM), (I2C, I2C), (DeviceFile, DeviceFile), (MCPChannel, MCPChannel),
    (PiPicoAnalog, PiPicoAnalog), (PiGPIO, PiGPIO))


class HardwareIOTypeForm(forms.Form):
    type = forms.ChoiceField(choices=hardware_io_choices)
    parent_hardware = forms.CharField()
    child_hardware = forms.CharField()
    child_channel = forms.CharField()
    hub = forms.CharField()
    parent_hardware.widget = forms.HiddenInput()
    child_hardware.widget = forms.HiddenInput()
    child_channel.widget = forms.HiddenInput()
    hub.widget = forms.HiddenInput()
    # def __init__(self, *args, **kwargs):
    #     super(HardwareTypeForm, self).__init__(*args, **kwargs)
    def __init__(self, *args, **kwargs):
        super(HardwareIOTypeForm, self).__init__(*args, **kwargs)


    class Meta:
        fields = ['type','parent_hardware','child_hardware','child_channel','hub']
