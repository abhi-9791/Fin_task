from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Employee
from rest_framework import status
from .serializers import Employee_Serializer
from django.http import Http404

class Employee_Details_By_Pk(APIView):
    """
    Thse API endpoint useful to retrieve, update or delete an employee instance.
    
    """   
    def get(self, request):
        """
        Retrieve an employee instance based on id.
        """
        try:
            regid = request.query_params.get('regid')
            if regid:
                pk = self.get_numeric_pk(regid)
                if pk:
                    employee = Employee.objects.get(pk=pk)
                    serializer_class = Employee_Serializer(employee)
            else:
                    employee = Employee.objects.all()
                    serializer_class = Employee_Serializer(employee,many=True)
            return Response({"message": "employee details found","success":True,"employees":serializer_class.data},status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({"message":"employee details not found","success":False,"employees":[]},status=status.HTTP_200_OK)
       
        except Exception as e:
                return Response({'message': "employee retreiving  failed","success":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get_numeric_pk(self, regid):
        # Example mapping function
        if regid.startswith('EMP'):
            try:
                numeric_part = int(regid[3:])
                return numeric_part
            except ValueError:
                pass
        return None
    def post(self,request):
        """
        Creating  a new employee.
        
        """
        try:
            serializer_class =  Employee_Serializer(data=request.data)
            # print(serializer_class)
            if serializer_class.is_valid():
                    ser = serializer_class.save()
                    regid = f"EMP{ser.id:03d}"
                    return Response({"message":"Employee created Suceefuly","regid":regid,'success':True},status=status.HTTP_201_CREATED)
            else:
                if "required" in serializer_class.errors or "parser"  in serializer_class.errors:
                    message = "Invalid body request"
                
                    response_data = {
                        "message": message,
                        "success": False
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                    
                return Response({"message":"employee exists already","success":False}, status=status.HTTP_200_OK)
                
        
        except Exception as exe:
            if 'JSON' in  str(exe):
                return Response({"message":"invalid Data","success":True},status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "employee created failed","success":True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self, request):
        """
        Update an employee instance based on id
        """
        regid = request.data.get('regid')
        if regid is None:
            response_data = {
                "message": "Invalid body request: 'regid' is missing",
                "success": False
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if regid:
                pk = self.get_numeric_pk(regid)
                employee = Employee.objects.get(pk=pk)
                print(employee)
                serializer_class = Employee_Serializer(employee, data=request.data)
                if serializer_class.is_valid():
                    ser=serializer_class.save()
                    print(ser)
                    data={
                        "message":"employee details updated successfully",
                        "success":True
                    }
                    return Response(data,status=status.HTTP_200_OK)
            else:
                return Response({"message":'provide empoyee id'},status=status.HTTP_204_NO_CONTENT)
                
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response({"message":"no employee found with this regid","success":False},status=status.HTTP_200_OK)
        except Exception as e:
            if 'JSON' in  str(e):
                return Response({"message":"invalid Data","success":False},status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': "employee updation failed","success":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        """
        Delete an employee instance.
        """
        regid = request.data.get('regid')
        if regid is None:
            response_data = {
                "message": "Invalid body request: 'regid' is missing",
                "success": False
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        try:
            pk = self.get_numeric_pk(regid)
            employee = Employee.objects.get(pk=pk)
            employee.delete()
            return Response({'message':'employee deleted successfully','success':True},status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response({'message':'no employee found with this regid','success':False},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message":"employee created failed","success":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)