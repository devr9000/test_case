from django.contrib import admin
from .models import Loading, LoadingMinerals, StorageResult, StorageMineralsResult, UnLoading

admin.site.register(Loading)
admin.site.register(LoadingMinerals)
admin.site.register(StorageMineralsResult)
admin.site.register(StorageResult)
admin.site.register(UnLoading)
