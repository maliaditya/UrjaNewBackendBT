from lib2to3.pytree import type_repr
from re import M
from chain_marketing_app.models import MemberAccount, BinaryTree, Payout, BinaryPayoutAttrs
from chain_marketing_app.serializers import PayoutSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework import serializers
import json
from background_task import background
from chain_marketing_app.models import BinaryTree


# On Cycle ends
# Traverse the tree form admin
# get each users left or right balance
# minus the greater balance from lesser balance
# give payout accordingly

# on Sale
# Give points to till parent w.r.t its left or right balance

# 100 points = 1 pair
# payable pairs = 1
# 1 point  = 1 


class BinaryTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BinaryTree
        fields = ['member','parent','is_active','is_admin','is_valid','left','right','left_points','right_points','position']

class TreeNode(dict):
    def __init__(self, name,attributes, children=None):
        super().__init__()
        self.__dict__ = self
        self.name = name
        self.attributes = attributes
        self.children = list(children) if children is not None else []

    @staticmethod
    def from_dict(dict_):
        node = TreeNode(dict_['name'], dict_['children'])
        node.children = list(map(TreeNode.from_dict, node.children))
        return node

class BinaryCyclePayouts(viewsets.ModelViewSet):
    queryset = BinaryTree.objects.all()
    serializer_class = BinaryTreeSerializer
    authentication_classes = []
    permission_classes = []
    ROOT = None
    CHILDREN = list()
    TEMP = list()
    get_payable_pair = 100 
    is_valid_member = True
    TwoIsToOnePayout = True
    file_ptr = open("Payout_logs","w")
    file = open('Binary_Payout_logs.txt','w')
    file.write("This is the write command\n")
    file.write("It allows us to write in a particular file\n")

    def get_binary_payout_attrs(self):
        attrs = BinaryPayoutAttrs.objects.get(is_active=True)
        return attrs

    def get_member_info(self, member_id):
        member = MemberAccount.objects.get(member_id=member_id)
        return member


    def is_active_sponser(self,member):
        active_sponser  =  BinaryTree.objects.get(member=member)
        if active_sponser.is_sponser_active and active_sponser.days > 2:
            active_sponser.is_sponser_active = False
            return False
        elif active_sponser.is_sponser_active and active_sponser.days < 2:
            return True
        else:
            return False

        #current
    def check_last_bt_payout(self,member):
        try:
            last_payout = Payout.objects.filter(member=member).order_by('-id')[0]
            # print("                        ")
            # print("check_last_bt_payout",last_payout,last_payout.created_at,last_payout.points,last_payout.type, last_payout.days<30)
            # print("                        ")
            return  last_payout.days<2
        except:
            return False


    def generate_payout(self, btmember, points):
                    intro = str(btmember).split(' ')
                    get_id = intro[2].split('(')
                    get_id = get_id[1].split(')')
                    get_id[0]
                    member = MemberAccount.objects.get(member_id=get_id[0])
                    tds=0
                    std_deduction=10
                    tds_payout = points*tds/100
                    std_payout = points*std_deduction/100
                    payout = points - tds_payout - std_payout
                    Payout( member=member,
                            from_member =member,
                            type = 'bt_payout',
                            name=member.get_user_name,
                            points=points,
                            tds=tds,
                            std_deduction=std_deduction,
                            payout=payout
                            ).save()
                    sponser = MemberAccount.objects.get(member_id=member.sponser_id)
                    self.check_last_bt_payout(sponser)
                    if self.check_last_bt_payout(member=sponser):
                        Payout( member=sponser,from_member =member,
                                        type = 'Sponser',
                                        name=sponser.get_user_name,
                                        points=points*25/100,
                                        tds=tds,
                                        std_deduction=std_deduction,
                                        payout=payout*25/100
                                        ).save()

    def check_valid_direct_members(self, member):
        
        valid_direct_member_Right =False
        valid_direct_member_Left = False
        direct_left_members= MemberAccount.objects.filter(sponser_id=member.member_id)
        for i in direct_left_members:
            btmember = BinaryTree.objects.get(member=i)
            if(btmember.position=='Left' and btmember.is_active):
                valid_direct_member_Left=True
            if(btmember.position=='Right' and btmember.is_active):
                valid_direct_member_Right=True
            
        return valid_direct_member_Right==valid_direct_member_Left
        

    def if_member_pass_1st_criteria(self, member,my_pay):

        # 2:1
        if member.left is  None or member.right is  None:
            return False
      
        if self.check_valid_direct_members(member):
           
            if member.left_points >0 and member.right_points >0:
                if  member.left_points >=self.get_payable_pair and member.right_points>=2*self.get_payable_pair:
                    member.left_points -=  self.get_payable_pair
                    member.right_points -= 2* self.get_payable_pair
                    member.is_valid = True
                    attrs = self.get_binary_payout_attrs()
                    self.generate_payout(member,(attrs.one_pair_value * my_pay))
                    member.save()
                    self.TwoIsToOnePayout = False
                    return True

                elif member.right_points >=self.get_payable_pair and member.left_points>=2*self.get_payable_pair: 
                    # member.right_points >=100* member.left_points>=2*100:
                    member.right_points -= self.get_payable_pair
                    member.left_points -=  2* self.get_payable_pair
                    member.is_valid = True
                    attrs = self.get_binary_payout_attrs()
                    self.generate_payout(member,(attrs.one_pair_value * my_pay))
                    member.save()
                    self.TwoIsToOnePayout = False
                    return True

    def calculate_payout(self,member,my_pay):
                memberAccMem =MemberAccount.objects.get(member_id=member)
                member = BinaryTree.objects.get(member=memberAccMem)
               
                if member.is_valid or self.if_member_pass_1st_criteria(member,my_pay):
                
                    member = BinaryTree.objects.get(member=memberAccMem)
                    if member.left_points >= member.right_points and member.right_points>0:
                            member.left_points -= member.right_points
                            member.right_points = 0
                            member.is_sponser_active = True
                            attrs = self.get_binary_payout_attrs()
                            if self.TwoIsToOnePayout:
                            	self.generate_payout(member,(attrs.one_pair_value *my_pay))
                            member.save()
                    elif member.right_points >= member.left_points and member.left_points>0:
                            member.right_points -= member.left_points
                            member.left_points =0
                            member.is_sponser_active = True
                            attrs = self.get_binary_payout_attrs()
                            if self.TwoIsToOnePayout:
                            	self.generate_payout(member,(attrs.one_pair_value *my_pay))
                            member.save()
                    else:
                            # member.right_points -= member.left_points
                            # member.left_points =0
                            # member.is_sponser_active = True
                            # attrs = self.get_binary_payout_attrs()
                            # print("else calculate_payout")
                            # self.generate_payout(member,(attrs.one_pair_value * my_pay))
                            # member.save()
                            pass


    def create_node(self,key,name,parent):
        if self.ROOT is  None:
            queryset = BinaryTree.objects.filter(parent=key)
            serializer_class = BinaryTreeSerializer(queryset, many=True)
            data = json.dumps(list(serializer_class.data))
            team = json.loads(data)
            self.ROOT = TreeNode(key,attributes={'name':name})
            self.get_childerns(self.ROOT,team)
        else:
            queryset = BinaryTree.objects.filter(parent=key)
            serializer_class = BinaryTreeSerializer(queryset, many=True)
            data = json.dumps(list(serializer_class.data))
            team = json.loads(data)
            parent.children.append(TreeNode(key,attributes={'name':name}))

    def get_childerns(self,parent,team):

        if len(team) >0:
            for i in team:
                member = BinaryTree.objects.get(member=MemberAccount.objects.get(member_id=i['member']))
                attrs = self.get_binary_payout_attrs()
                if member.left_points >=(attrs.one_pair) and member.right_points >=(attrs.one_pair):
                    if member.left_points>member.right_points:
                        if int(member.right_points/attrs.one_pair) > attrs.payable_pairs:
                            self.calculate_payout(i['member'],( attrs.payable_pairs)) 
                        else:
                            self.calculate_payout(i['member'],(int(member.right_points/attrs.one_pair))) 
                    else:
                        if int(member.left_points/attrs.one_pair) > attrs.payable_pairs:
                            self.calculate_payout(i['member'],( attrs.payable_pairs)) 
                        else:
                            self.calculate_payout(i['member'],(int(member.left_points/attrs.one_pair))) 
                self.CHILDREN.append(i['member'])
                self.create_node(key=i['member'], name=self.get_member_info(member_id=i['member']).get_user_name,parent=parent)
        if len(parent.children) > 0:
                self.TEMP.extend(self.CHILDREN)
                self.CHILDREN.clear()
                for child in parent.children:
                    for key in set(self.TEMP):
                        if child.name == key:
                            queryset = BinaryTree.objects.filter(parent=key)
                            serializer_class = BinaryTreeSerializer(queryset, many=True)
                            data = json.dumps(list(serializer_class.data))
                            team = json.loads(data)
                            self.get_childerns(child,team)

    def insert(self,key,name):
        if self.ROOT is None:
            self.create_node(key=key,name=name,parent=self.ROOT)

    def list(self, request):
        self.file_ptr.write("in list intial call")
        self.file.write("It allows us to write in a particular file")
        self.TEMP.clear()
        starting_node = MemberAccount.objects.get(is_admin=True).member_id
        queryset = BinaryTree.objects.get(member=starting_node)
        name = self.get_member_info(member_id=starting_node).get_user_name
        self.insert(key=starting_node,name=name)
        if self.ROOT is not None:
            return Response(json.loads(json.dumps(self.ROOT, indent=2)),status=status.HTTP_200_OK)
        self.file_ptr.close()
        return Response({"message":"success"},status=status.HTTP_200_OK)
        
    file.close()
