from rest_framework import serializers
from .models import( Payout, MemberAccount,ActiveMember,AddProduct,Level, Image,Order, OrderDetails, Sale,ActiveCityDistibuter,ActiveSeller,ActiveTalukaDistibuter,ActiveDistrictDistibuter
,ActiveDistrictDistibuter
,ActiveTalukaDistibuter
,ActiveCityDistibuter
,ActiveSeller
,ActiveMember
,Introducer,District, City, Taluka,SubProductsStock,BankDetails,
SubProductsSale,
BinaryTree,
AllMembersProductStock
)

class AllMembersProductStockSerializer(serializers.ModelSerializer):
    # app_owned = ApplicationOwnedSerializer(read_only=True)
    class Meta:
        model = AllMembersProductStock
        fields ='__all__'

class BinaryTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BinaryTree
        fields = ['id','member','parent','is_active','is_admin','is_valid','left','right','left_points','right_points','position']

class SubProductsSaleSerializer(serializers.ModelSerializer):
    # app_owned = ApplicationOwnedSerializer(read_only=True)
    class Meta:
        model = SubProductsSale
        fields = '__all__'

class BankDetailsSerializer(serializers.ModelSerializer):
    # app_owned = ApplicationOwnedSerializer(read_only=True)
    class Meta:
        model = BankDetails
        fields = '__all__'


class SubProductsStockSerializer(serializers.ModelSerializer):
    # app_owned = ApplicationOwnedSerializer(read_only=True)
    class Meta:
        model = SubProductsStock
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    # app_owned = ApplicationOwnedSerializer(read_only=True)
    class Meta:
        model = City
        fields ='city',


class TalukaSerializer(serializers.ModelSerializer):
    # app_owned = ApplicationOwnedSerializer(read_only=True)
    taluka_city =CitySerializer(many=True, read_only=True)

    class Meta:
        model = Taluka
        fields ='taluka','taluka_city'


class DistrictSerializer(serializers.ModelSerializer):
    # app_owned = ApplicationOwnedSerializer(read_only=True)
    district_taluka =TalukaSerializer(many=True, read_only=True)
    class Meta:
        model = District
        fields ='district','district_taluka'


class IntroducerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Introducer
        fields =['introducer', 'distributer' ]
        # depth=1


class IntroducerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Introducer
        fields =['introducer', 'distributer' ]
        depth=1


class SellersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveSeller
        fields = ['seller','is_active','get_created_at','get_updated_at']



class SaleListSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    member = serializers.StringRelatedField()
    class Meta:
        model = Sale
        fields = ['member','product','get_created_at','get_updated_at']


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['seller','member','product','get_created_at','get_updated_at']


class PayoutSerializer(serializers.ModelSerializer):
    from_member = serializers.StringRelatedField()
    member = serializers.StringRelatedField()
    class Meta:
        model = Payout
        fields = ['id','member','points','tds','std_deduction','payout','from_member','type','payment','description','declared','get_created_at','get_updated_at','created_at']

class LevelSerializer(serializers.ModelSerializer):
    # app_owned = ApplicationOwnedSerializer(read_only=True)
    class Meta:
        model = Level
        fields = ['level','points']

class CountSerializer(serializers.ModelSerializer):
    
    # app_owned = ApplicationOwnedSerializer(read_only=True)
    class Meta:
        model = MemberAccount
        fields = ['get_total_members',]

class OrderDetailsSerializer(serializers.ModelSerializer):
    # app_owned = ApplicationOwnedSerializer(read_only=True)
    class Meta:
        model = OrderDetails
        fields =['id','product','quantity','price','product_id','order_by','quantity_delivered','quantity_undelivered','quantity_sold','generated','transfer_in','transfer_out','is_generated','is_transfer']

class StockSerializer(serializers.ModelSerializer):
    # app_owned = ApplicationOwnedSerializer(read_only=True)
    class Meta:
        model = OrderDetails
        fields ='__all__'

class ImageSerializer(serializers.ModelSerializer):
    # app_owned = ApplicationOwnedSerializer(read_only=True)
    class Meta:  
        model = Image
        fields = ['product','image']

class AddProductSerializer(serializers.ModelSerializer):
    # product_image = ImageSerializer(many=True)
    levels = LevelSerializer(many=True)
    class Meta:
        model = AddProduct
        fields = ['id','name','created_by','description','is_published','Price','product_type','max_payout','active25_bonus','seller_bonus','MRP','levels','points_to_city_distributer','has_key','points_to_taluka_distributer','points_to_district_distributer','points_to_buyer','is_package_product','is_package','add_package_product','quantity']

    def create(self, validated_data):
        levels = validated_data.pop('levels')
        product = AddProduct.objects.create(**validated_data)
        for level in levels:
            Level.objects.create( product=product,**level)
        return product

class OrderSerializer(serializers.ModelSerializer):
    order_detail = OrderDetailsSerializer(many=True)
    class Meta:
        model = Order
        fields = ['ordered_from','orded_by','total_amount','is_paid','status','delivery','get_created_at','get_updated_at','order_detail','is_generated','is_transfer']

    def create(self, validated_data):
        order_details = validated_data.pop('order_detail')
        order = Order.objects.create(**validated_data)
        for order_detail in order_details:
            OrderDetails.objects.create( order=order,**order_detail)
        return order

    def update(self, instance, validated_data):
        instance.is_paid = validated_data.get('is_paid')
        instance.status = validated_data.get('status')
        instance.delivery = validated_data.get('delivery')
        instance.save()
        return instance

class OrderListSerializer(serializers.ModelSerializer):
    orded_by =  serializers.StringRelatedField()
    order_detail = serializers.SerializerMethodField()
    is_paid = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['order_no','ordered_from','orded_by','total_amount','is_paid','get_created_at','get_updated_at','order_detail','status','delivery','is_generated','is_transfer']

    def get_order_detail(self, obj):
        return int(obj.order_detail.count())

    def get_is_paid(self, obj):
        if bool(obj.is_paid):
            return 'Yes'
        return 'No'



class ActiveMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveMember
        fields = 'is_active',
    

class ActiveMemberNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveMember
        fields = [],
        

class ActiveCityDistibuterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveCityDistibuter
        fields = 'is_active','city','pin_code'



# class ActiveSellerNewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ActiveSeller
#         fields = [],


class ActiveSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveSeller
        fields = 'is_active', 'bonus_points'


class ActiveTalukaDistibuterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveTalukaDistibuter
        fields = 'is_active',



class ActiveDistrictDistibuterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveDistrictDistibuter
        fields = 'is_active',

class MemberAccountSerializer(serializers.ModelSerializer):
    # active_member =ActiveMemberNewSerializer()
    # active_city = ActiveCityDistibuterSerializer()
    # active_seller = ActiveSellerNewSerializer()
    # active_taluka = ActiveTalukaDistibuterSerializer()
    # active_district = ActiveDistrictDistibuterSerializer()
    
    class Meta:

        model = MemberAccount
        # fields =['user','sponser_id','member_id','taluka','district','city','pin_code','is_admin','get_created_at','get_updated_at',
        #             'get_user_name','active_taluka','active_city','active_district','active_seller','active_member'  ]
        fields =['user','sponser_id','member_id','pin_code' ,'left', 'right']
    
    def create(self, validated_data):
            # active_member = validated_data.pop('active_member')
            # active_seller = validated_data.pop('active_seller')
            # active_city = validated_data.pop('active_city')
            # active_taluka = validated_Pdata.pop('active_taluka')
            # active_district = validated_data.pop('active_district')
            pin_code = validated_data.pop('pin_code')
            left = validated_data.pop('left')
            right = validated_data.pop('right')

            member_account = MemberAccount.objects.create(**validated_data)
            sponser_id = validated_data.pop('sponser_id')
            btParent = BinaryTree.objects.get(member=sponser_id)
            sponser = MemberAccount.objects.get(member_id=sponser_id)
            ActiveMember.objects.create( member=member_account,is_active = False)
            ActiveSeller.objects.create( seller=member_account,is_active = False)
            ActiveCityDistibuter.objects.create( distributer=member_account,is_active = False,city = '',pin_code=pin_code)
            if left:
                print("in serializer left if")
                # if left of parent is null the allocate the child directly to the parent
                if btParent.left==None:
                    btParent.left = member_account
                    btParent.save()

                    # adding child into the binary tree
                    BinaryTree.objects.create(member=member_account,parent=btParent.member,is_active=False,position='Left')

                else:

                    # if parent left node is not null the itereate over the tree tiil we get to its extreme ledt node where the left node is null
                    while btParent.left!=None:

                        # Spliting string representation of the member to its id = aditya mali (URJAB22H86) --> URJAB22H86
                        intro = str(btParent.left).split(' ')
                        get_id = intro[2].split('(')
                        get_id = get_id[1].split(')')

                        # seting btParent to its left child
                        btParent =BinaryTree.objects.get(member = get_id[0])
                    
                    if btParent.left==None:
                        btParent.left = member_account
                        btParent.save()
                        BinaryTree.objects.create(member=member_account,parent=btParent.member,is_active=False,position='Left')
            else:
                print("in serializer else")
                # if right of parent is null the allocate the child directly to the parent
                if btParent.right==None:
                    btParent.right = member_account
                    btParent.save()

                    # adding child into the binary tree
                    BinaryTree.objects.create(member=member_account,parent=btParent.member,is_active=False,position='Right')

                else:
                    # if parent right node is not null the itereate over the tree tiil we get to its extreme right node where the left node is null
                    while btParent.right!=None:

                        # Spliting string representation of the member to its id = aditya mali (URJAB22H86) --> URJAB22H86
                        intro = str(btParent.right).split(' ')
                        get_id = intro[2].split('(')
                        get_id = get_id[1].split(')')
                        
                        # seting btParent to its right child
                        btParent = BinaryTree.objects.get(member= get_id[0])

                    if btParent.right==None:
                        btParent.right = member_account
                        btParent.save()
                        BinaryTree.objects.create(member=member_account,parent=btParent.member,is_active=False,position='Right')
        
            return member_account
        


class MemberAccountListSerializer(serializers.ModelSerializer):
    active_member =ActiveMemberSerializer(many=True, read_only=True)
    active_city = ActiveCityDistibuterSerializer(many=True, read_only=True)
    active_seller = ActiveSellerSerializer(many=True, read_only=True)
    active_taluka = ActiveTalukaDistibuterSerializer(many=True, read_only=True)
    active_district = ActiveDistrictDistibuterSerializer(many=True, read_only=True)
    
    class Meta:
        model = MemberAccount
        fields =['user','sponser_id','member_id','taluka','district','city','pin_code','is_admin','get_created_at','get_updated_at',
                    'get_user_name','active_taluka','active_city','active_district','active_seller','active_member'  ]

    # def get_active_city(self, obj):
    #     return bool(obj.active_city)

    # def get_active_seller(self, obj):
    #     return bool(obj.active_seller)

    # def get_active_taluka(self, obj):
    #     return bool(obj.active_taluka)

    # def get_active_district(self, obj):
    #     return bool(obj.active_district)

