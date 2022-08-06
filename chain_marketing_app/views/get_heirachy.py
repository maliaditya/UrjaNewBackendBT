from chain_marketing_app.models import MemberAccount
from rest_framework import  status, viewsets
from rest_framework.response import Response
from rest_framework import serializers
import json

class MemberAccountSerializer(serializers.ModelSerializer):
    # app_owned = ApplicationOwnedSerializer(read_only=True)
    class Meta:
        model = MemberAccount
        fields = ['sponser_id', 'member_id','get_user_name']

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

class GetHeirachy(viewsets.ModelViewSet):
    queryset = MemberAccount.objects.all()
    serializer_class = MemberAccountSerializer
    authentication_classes = []
    permission_classes = []
    ROOT = None
    CHILDREN = list()
    TEMP = list()

    def create_node(self,key,name,parent):
        if self.ROOT is  None:
            queryset = MemberAccount.objects.filter(sponser_id=key)
            serializer_class = MemberAccountSerializer(queryset, many=True)
            data = json.dumps(list(serializer_class.data))
            team = json.loads(data)
            self.ROOT = TreeNode(key,attributes={'name':name,'team':len(team)})
            print(self.get_childerns(self.ROOT,team))
        else:
            queryset = MemberAccount.objects.filter(sponser_id=key)
            serializer_class = MemberAccountSerializer(queryset, many=True)
            data = json.dumps(list(serializer_class.data))
            team = json.loads(data)
            parent.children.append(TreeNode(key,attributes={'name':name,'team':len(team)}))

    def get_childerns(self,parent,team):
        if len(team) >0:
            for i in team:
                print(i)
                self.CHILDREN.append(i['member_id'])
                self.create_node(key=i['member_id'], name=i['get_user_name'],parent=parent)
        if len(parent.children) > 0:
                self.TEMP.extend(self.CHILDREN)
                self.CHILDREN.clear()
                for child in parent.children:
                    for key in set(self.TEMP):
                        if child.name == key:
                            queryset = MemberAccount.objects.filter(sponser_id=key)
                            serializer_class = MemberAccountSerializer(queryset, many=True)
                            data = json.dumps(list(serializer_class.data))
                            team = json.loads(data)
                            self.get_childerns(child,team)
        
    def insert(self,key,name):
        if self.ROOT is None:
            self.create_node(key=key,name=name,parent=self.ROOT)

    def list(self, request):
        self.TEMP.clear()
        starting_node = request.query_params.get('member')
        queryset = MemberAccount.objects.get(member_id=starting_node)
        name = queryset.get_user_name
        self.insert(key=starting_node,name=name)
        print(self.TEMP)
        if self.ROOT is not None:
            return Response(json.loads(json.dumps(self.ROOT, indent=2)),status=status.HTTP_200_OK)