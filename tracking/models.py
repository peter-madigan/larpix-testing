from django.db import models

status_key_list = [
    ('F', 'Fail'),
    ('P', 'Pass'),
    ('W', 'Weird')
    ]

class LArPixDBObject(models.Model):
    '''                                                                                            
    Base class for database entries                                                                
    '''
    entry_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        string = '{}('
        string += 'entry_date={entry_date}, '
        string += 'note={note}'
        string += ')'
        return string.format(type(self).__name__, **vars(self))

class ASIC(LArPixDBObject):
    '''
    Base class for LArPix ASICs
    '''
    _avail_versions = [
        ('1','LArPix v1'),
        ('2','LArPix v2')
        ]

    status = models.CharField(max_length=100, choices=status_key_list)
    packaged = models.BooleanField(default=False)
    version = models.CharField(max_length=100, choices=_avail_versions)
    test_results = models.ManyToManyField('TestResult', blank=True)
    #pcb = models.ManyToManyField('PCB', through='Connection')

    def __str__(self):
        string = super().__str__()[:-1]
        string += ', '
        string += 'version={version}, '
        string += 'packaged={packaged}, '
        string += 'status={status}'
        string += ')'
        return string.format(**vars(self))

class PCB(LArPixDBObject):
    '''
    Base class for test boards
    '''
    _avail_versions = [
        ('4c-hpats','4-chip high purity argon test stand anode'),
        ('28c-hpats','28-chip high purity argon test stand anode')
        ]
    status = models.CharField(max_length=100, choices=status_key_list)
    version = models.CharField(max_length=100, choices=_avail_versions)
    test_results = models.ManyToManyField('TestResult', blank=True)
    asics = models.ManyToManyField('ASIC', through='Connection', blank=True)

    def __str__(self):
        string = super().__str__()[:-1]
        string += ', '
        string += 'version={version}, '
        string += 'status={status}'
        string += ')'
        return string.format(**vars(self))

class TestResult(LArPixDBObject):
    '''
    Base class for test results
    '''
    _avail_names = [
        ('noise-test-v1','Standard noise test')
        ]
    result = models.CharField(max_length=100, choices=status_key_list)
    name = models.CharField(max_length=100, choices=_avail_names)
    asics = models.ManyToManyField('ASIC', blank=True)
    pcbs = models.ManyToManyField('PCB', blank=True)

    def __str__(self):
        string = super().__str__()[:-1]
        string += ', '
        string += 'name={name}, '
        string += 'result={result}'
        string += ')'
        return string.format(**vars(self))

class NoiseTestResult(TestResult):
    '''
    Model for standard noise test results
    '''
    test_result = models.OneToOneField('TestResult', on_delete=models.CASCADE, parent_link=True)

class Connection(LArPixDBObject):
    '''
    Model for creating assiociations between chips and PCBs
    '''
    position = models.IntegerField(blank=True, null=True)

    pcb = models.ForeignKey('PCB', on_delete=models.CASCADE)
    asic = models.ForeignKey('ASIC', on_delete=models.CASCADE)

    def __str__(self):
        string = super().__str__()[:-1]
        string += ', '
        string += 'pcb={pcb}, '
        string += 'position={position}, '
        string += 'asic={asic}'
        string += ')'
        return string.format(**vars(self))
