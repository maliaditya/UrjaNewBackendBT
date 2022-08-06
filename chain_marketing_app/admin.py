from django.contrib import admin,messages

# Then, when you need to error the user:
from .models import (ActiveCityDistibuter, ActiveMember, ActiveSeller, MemberAccount,AddProduct,MemberActivationKey,Order,Level, Payout,OrderDetails,Sale,CommonFields
,ActiveCityDistibuter,Introducer, City, Taluka, District,AdminAccounts,BankDetails,SubProductsStock, BinaryTree,BinaryPayoutAttrs,Test,IntroducerRequest)

admin.site.register(Test)
#admin.site.register(IntroducerRequest)

# @admin.register(City)
# class CityAdmin(admin.ModelAdmin):
#     list_display = ('taluka','city')
@admin.register(IntroducerRequest)
class IntroducerRequestAttrs(admin.ModelAdmin):
        list_display =['introducer','distributer','status','active_status']

@admin.register(BinaryPayoutAttrs)
class BinaryPayoutAttrs(admin.ModelAdmin):
    list_display =['one_pair','payable_pairs','one_pair_value','is_active']

@admin.register(BinaryTree)
class BinaryTree(admin.ModelAdmin):
    list_display =['member','parent','is_active','is_valid','left','right','left_points','right_points','position','is_sponser_active','updated_at']

@admin.register(BankDetails)
class BankDetails(admin.ModelAdmin):
    list_display = ('user','member','created_at','updated_at','upi','bank_name','bank_branch','bank_account','bank_ifsc','nominee')
    search_fields = ('member',)
    
# @admin.register(Taluka)
# class TalukaAdmin(admin.ModelAdmin):
#     list_display = ('district','taluka')

# @admin.register(District)
# class DistrictAdmin(admin.ModelAdmin):
#     list_display = ('district',)


@admin.register(MemberAccount)
class MemberAccountAdmin(admin.ModelAdmin):
    list_display = ('user','sponser_id','member_id','taluka','is_admin')
    search_fields = ('member_id',)

@admin.register(Introducer)
class IntroducerAdmin(admin.ModelAdmin):
    list_display = ('introducer','distributer')

# @admin.register(MemberActivationKey)
# class MemberActivationKeyAdmin(admin.ModelAdmin):
#     list_display = ('allocated_to','key' , 'is_active')


@admin.register(AddProduct)
class AddproductAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('ordered_from','orded_by','total_amount','is_paid','created_at','updated_at','status','delivery')


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('product','level','points')
    
@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    actions = ['declare_selected', 'undeclare_selected','declare_payments','get_total_payment','undeclare_payments','make_tds_zero']
    list_display = ('member','name','points','from_member','type','tds','std_deduction','payout','payment','declared','created_at' )
    list_filter = ('created_at','declared')
    search_fields=('name','created_at','member__member_id')
    def declare_selected(self, request, queryset):
        queryset.update(declared=True)
    declare_selected.short_description = "Declare the selected payouts"

    def undeclare_selected(self, request, queryset):
        queryset.update(declared=False)
    undeclare_selected.short_description = "Undeclare the selected payouts"

    def declare_payments(self, request, queryset):
        for q in queryset:
            if q.declared == False:
                return messages.error(request, "Declare the payout first") 
            q.payment = q.payout
            q.declared=True
            q.save()
        return messages.success(request, "Payments declared") 
    declare_payments.short_description = "Declare the selected payments"

    def undeclare_payments(self, request, queryset):
        for q in queryset:
            if q.declared == False:
                return messages.error(request, "Declare the payout first") 
            q.payment = 0
            q.declared=True
            q.save()
        return messages.success(request, "Payments declared") 
    undeclare_payments.short_description = "Undeclare the selected payments"


    def get_total_payment(self, request, queryset):
        total = 0
        for q in queryset:
            total += q.payout
        return messages.add_message(request,messages.INFO, f"Total Pending Payment : {total}") 
    get_total_payment.short_description = "Get Total Pending Payment"

    def make_tds_zero(self, request, queryset):
        for q in queryset:
            tds_to_be_added = q.points*q.tds/100
            q.tds = 0
            q.payout += tds_to_be_added 
            q.save()

    get_total_payment.short_description = "make tds zero"


@admin.register(ActiveMember)
class ActiveMemberAdmin(admin.ModelAdmin):
    list_display = ('member','is_active','created_at','updated_at' )
    

@admin.register(ActiveSeller)
class ActiveSellerAdmin(admin.ModelAdmin):
    list_display = ('seller','is_active' ,'bonus_points','created_at','updated_at')


@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('order','order_by','quantity','price','quantity_delivered','quantity_undelivered','quantity_sold')



@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('member','product','created_at','updated_at','created_at','updated_at')

    
@admin.register(ActiveCityDistibuter)
class ActiveCityDistibuterAdmin(admin.ModelAdmin):
    list_display = ('distributer','city','pin_code','is_active','created_at','updated_at')

    
# @admin.register(CommonFields)
# class CommonFieldsrAdmin(admin.ModelAdmin):
#     list_display = ('seller_bonus','introducer_bonus','is_active')

    
@admin.register(AdminAccounts)
class AdminAccountsAdmin(admin.ModelAdmin):
    list_display = ('dp','total_payout','difference','distributed_payout','bonus','balance_after_deduction','tds','std','total_balance')

@admin.register(SubProductsStock)
class AdminSubProductsStock(admin.ModelAdmin):
    list_display = ('member','product','quantity')
