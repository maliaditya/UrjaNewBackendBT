from chain_marketing_app.models import MemberAccount, BinaryTree
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework import serializers
import json


class BinaryTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BinaryTree
        fields = ['member','parent','is_active','is_admin','left','right','left_points','right_points']


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

class GetBinaryTreeHeirachy(viewsets.ModelViewSet):
    queryset = BinaryTree.objects.all()
    serializer_class = BinaryTreeSerializer
    authentication_classes = []
    permission_classes = []
    ROOT = None
    CHILDREN = list()
    TEMP = list()

    def get_member_info(self, member_id):
        member = MemberAccount.objects.get(member_id=member_id)
        return member



    def create_node(self,key,name,parent,left_points=None, right_points=None,is_valid=None,is_active=None,sponser=None):
        if self.ROOT is  None:
            queryset = BinaryTree.objects.filter(parent=key)
            serializer_class = BinaryTreeSerializer(queryset, many=True)
            data = json.dumps(list(serializer_class.data))
            team = json.loads(data)
            self.ROOT = TreeNode(key,attributes={'Name':name,'Left Points':left_points,'Right Points':right_points,'is_valid':is_valid,'is_active':is_active,'sponser':self.get_sponser_of_current_member(key)})
            self.get_childerns(self.ROOT,team)
        else:
            queryset = BinaryTree.objects.filter(parent=key)
            serializer_class = BinaryTreeSerializer(queryset, many=True)
            data = json.dumps(list(serializer_class.data))
            team = json.loads(data)
            parent.children.append(TreeNode(key,attributes={'Name':name,'Left Points':left_points,'Right Points':right_points,'is_valid':is_valid,'is_active':is_active,'sponser':self.get_sponser_of_current_member(key)}))

    def get_left_points(self,member):
        return BinaryTree.objects.get(member=member).left_points
    
    def get_right_points(self,member):
        return BinaryTree.objects.get(member=member).right_points

        
    def get_is_valid(self,member):
        return BinaryTree.objects.get(member=member).is_valid
    
    def get_is_active(self,member):
        return BinaryTree.objects.get(member=member).is_active


    def get_childerns(self,parent,team):
        if len(team)==1:
            team.append({"member":0})
        if len(team)==2:
            if BinaryTree.objects.get(member=parent.get('name')).left == MemberAccount.objects.get(member_id=team[0]['member']) :
                    i =team[0]
                    self.CHILDREN.append(team[0]['member'])
                    self.create_node(key=team[0]['member'], name=self.get_member_info(member_id=team[0]['member']).get_user_name,parent=parent,
                                                                    left_points=self.get_left_points(i['member']), right_points=self.get_right_points(i['member']),is_valid=self.get_is_valid(i['member']),
                                                                    is_active=self.get_is_active(i['member']),sponser=self.get_sponser_of_current_member(team[0]['member']))

            elif team[1]['member']!=0 and  BinaryTree.objects.get(member=parent.get('name')).left == MemberAccount.objects.get(member_id=team[1]['member']) :
                    if team[1]['member']!=0:
                        i =team[1]
                        self.CHILDREN.append(team[1]['member'])
                        self.create_node(key=team[1]['member'], name=self.get_member_info(member_id=team[1]['member']).get_user_name,parent=parent,
                                                                        left_points=self.get_left_points(i['member']), right_points=self.get_right_points(i['member']),is_valid=self.get_is_valid(i['member']),
                                                                        is_active=self.get_is_active(i['member']),sponser=self.get_sponser_of_current_member(team[0]['member']))
            elif  team[1]['member']==0:
                parent.children.append(TreeNode('Empty',attributes={}))


            if BinaryTree.objects.get(member=parent.get('name')).right == MemberAccount.objects.get(member_id=team[0]['member']):
                    i =team[0]
                    self.CHILDREN.append(team[0]['member'])
                    self.create_node(key=team[0]['member'], name=self.get_member_info(member_id=team[0]['member']).get_user_name,parent=parent,
                                                                    left_points=self.get_left_points(i['member']), right_points=self.get_right_points(i['member']),is_valid=self.get_is_valid(i['member']),
                                                                    is_active=self.get_is_active(i['member']),sponser=self.get_sponser_of_current_member(team[0]['member']))

            elif team[1]['member']!=0 and BinaryTree.objects.get(member=parent.get('name')).right == MemberAccount.objects.get(member_id=team[1]['member']) :
                 if team[1]['member']!=0:
                    i =i =team[1]
                    self.CHILDREN.append(team[1]['member'])
                    self.create_node(key=team[1]['member'], name=self.get_member_info(member_id=team[1]['member']).get_user_name,parent=parent,
                                                                    left_points=self.get_left_points(i['member']), right_points=self.get_right_points(i['member']),is_valid=self.get_is_valid(i['member']),
                                                                    is_active=self.get_is_active(i['member']),sponser=self.get_sponser_of_current_member(team[0]['member']))
            elif  team[1]['member']==0:
                    parent.children.append(TreeNode('Empty',attributes={}))
                                                
        elif len(team)==1:
            i =team[0]
            self.CHILDREN.append(team[0]['member'])
            self.create_node(key=team[0]['member'], name=self.get_member_info(member_id=team[0]['member']).get_user_name,parent=parent,
                                                            left_points=self.get_left_points(i['member']), right_points=self.get_right_points(i['member']),
                                                            is_valid=self.get_is_valid(i['member']),is_active=self.get_is_active(i['member']),sponser=self.get_sponser_of_current_member(team[0]['member']))
        
        # if len(team) >0:
        #     for i in team:
        #         self.CHILDREN.append(i['member'])
        #         self.create_node(key=i['member'], name=self.get_member_info(member_id=i['member']).get_user_name,parent=parent,
        #                                         left_points=self.get_left_points(i['member']), right_points=self.get_right_points(i['member']),is_valid=self.get_is_valid(i['member']))

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

    def insert(self,key,name,left_points=None, right_points=None,is_valid=None,is_active=None,sponser=None):
        if self.ROOT is None:
            self.create_node(key=key,name=name,parent=self.ROOT,left_points=left_points, right_points=right_points, is_valid=is_valid,is_active=is_active,sponser=sponser)

    def get_sponser_of_current_member(self,member):
        sponser = MemberAccount.objects.get(member_id=member).sponser_id
        return sponser

    def list(self, request):
        self.TEMP.clear()
        starting_node = request.query_params.get('member')
        self.get_sponser_of_current_member(starting_node)
        queryset = BinaryTree.objects.get(member=starting_node)
        name = self.get_member_info(member_id=starting_node).get_user_name
        self.insert(key=starting_node,name=name,left_points=queryset.left_points, right_points=queryset.right_points, is_valid=queryset.is_valid, is_active=queryset.is_active, sponser=self.get_sponser_of_current_member(starting_node))
        if self.ROOT is not None:
            return Response(json.loads(json.dumps(self.ROOT, indent=2)),status=status.HTTP_200_OK)
        return Response({"message":"success"},status=status.HTTP_200_OK)