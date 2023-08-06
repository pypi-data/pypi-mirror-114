from django.contrib.auth.models import User
from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse

import unittest

def login_user(c: object, self: object) -> object:
    response = c.post(
        reverse('login'),
        self.credentials,
        follow=True,
    )
    self.assertTrue(response.context['user'].is_active)


class AdminUserPermissionTest(TestCase):
    """
    The admin user will have full access to the whole site - even if they are not associated with
    a group that is associated with the object.
    """
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': 'admin',
            'password': 'Test1234$'
        }

    def test_project_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)


        # Make sure the admin user can open up the project
        response = c.get(reverse('project_information', args=['1']))
        self.assertEqual(response.status_code, 200)
        print("Admin user can access a project with overlapping groups")

        # Make sure the admin user can open up the project
        response = c.get(reverse('project_information', args=['2']))
        self.assertEqual(response.status_code, 200)
        print("Admin user can access a project without overlapping groups")

        c.get(reverse('logout'))

    def test_task_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open up the task
        response = c.get(reverse('task_information', args=['1']))
        self.assertEqual(response.status_code, 200)
        print("Admin user can access a task with overlapping groups")

        # Make sure the admin user can open up the project
        response = c.get(reverse('task_information', args=['2']))
        self.assertEqual(response.status_code, 200)
        print("Admin user can access a task without overlapping groups")

        c.get(reverse('logout'))

    def test_kanban_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open the kanban
        response = c.get(reverse('kanban_information', args=[1]))
        self.assertEqual(response.status_code, 200)
        print("Admin user can access a kanban board with overlapping groups")

        # Make sure the admin user can open the kanban
        response = c.get(reverse('kanban_information', args=[2]))
        self.assertEqual(response.status_code, 200)
        print("Admin user can access a kanban board without overlapping groups")


    def test_new_organisation_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open the kanban
        response = c.get(reverse('new_organisation'))
        self.assertEqual(response.status_code, 200)
        print("Admin user can access a new_organisation with overlapping groups")

    def test_organisation_information_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open the kanban
        response = c.get(reverse('organisation_information', args=[1]))
        self.assertEqual(response.status_code, 200)
        print("Admin user can access a organisation_information with overlapping groups")


class TeamLeaderPermissionTest(TestCase):
    """
    The team leader will only have access to objects that have at least one cross over group with that
    particular team leader.
    """
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': 'team_leader',
            'password': 'Test1234$'
        }

    def test_project_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open up the project
        response = c.get(reverse('project_information', args=['1']))
        self.assertEqual(response.status_code, 200)
        print("Team Leader can access a project with overlapping groups")

        # # Make sure the admin user can open up the project
        # response = c.get(reverse('project_information', args=['2']))
        # self.assertEqual(response.status_code, 403)
        # print("Team Lead can NOT access a project without overlapping groups")

        c.get(reverse('logout'))

    def test_task_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open up the project
        response = c.get(reverse('task_information', args=['1']))
        self.assertEqual(response.status_code, 200)
        print("Team Leader can access a task with overlapping groups")

        # # Make sure the admin user can open up the project
        # response = c.get(reverse('task_information', args=['2']))
        # self.assertEqual(response.status_code, 403)
        # print("Team Lead can NOT access a task without overlapping groups")

        c.get(reverse('logout'))

    def test_kanban_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open the kanban
        response = c.get(reverse('kanban_information', args=[1]))
        self.assertEqual(response.status_code, 200)
        print("Team Leader can access a kanban board with overlapping groups")

        # Make sure the admin user can open the kanban
        response = c.get(reverse('kanban_information', args=[2]))
        self.assertEqual(response.status_code, 403)
        print("Team Leader can access a kanban board without overlapping groups")

    def test_new_organisation_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open the kanban
        response = c.get(reverse('new_organisation'))
        self.assertEqual(response.status_code, 200)
        print("Admin user can access a new_organisation with overlapping groups")

    def test_organisation_information_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open the kanban
        response = c.get(reverse('organisation_information', args=[1]))
        self.assertEqual(response.status_code, 200)
        print("Admin user can access a organisation_information with overlapping groups")


class TeamMemberPermissionTest(TestCase):
    """
    The team MEMBER will only have access to objects that have at least one cross over group with that
    particular team leader.
    """
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': 'team_member',
            'password': 'Test1234$'
        }

    def test_project_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open up the project
        response = c.get(reverse('project_information', args=['1']))
        self.assertEqual(response.status_code, 200)
        print("Team Member can access a project with overlapping groups")

        # # Make sure the admin user can open up the project
        # response = c.get(reverse('project_information', args=['2']))
        # self.assertEqual(response.status_code, 403)
        # print("Team Member can NOT access a project without overlapping groups")

        c.get(reverse('logout'))

    def test_task_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open up the project
        response = c.get(reverse('task_information', args=['1']))
        self.assertEqual(response.status_code, 200)
        print("Team Member can access a task with overlapping groups")

        # # Make sure the admin user can open up the task
        #response = c.get(reverse('task_information', args=['2']))
        #self.assertEqual(response.status_code, 403)
        #print("Team Member can NOT access a task without overlapping groups")

        c.get(reverse('logout'))

class TeamInternPermissionTest(TestCase):
    """
    The team leader will only have access to objects that have at least one cross over group with that
    particular team leader.
    """
    fixtures = ['NearBeach_basic_setup.json']

    def setUp(self):
        self.credentials = {
            'username': 'team_intern',
            'password': 'Test1234$'
        }

    def test_project_permissions_ti(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open up the project
        response = c.get(reverse('project_information', args=['1']))
        self.assertEqual(response.status_code, 200)
        print("Team Intern can access a project with overlapping groups")

        # # Make sure the admin user can open up the project
        #response = c.get(reverse('project_information', args=['2']))
        #self.assertEqual(response.status_code, 403)
        #print("Team Intern can NOT access a project without overlapping groups")

        c.get(reverse('logout'))

    def test_task_permissions(self):
        c = Client()

        # User will be logged in
        login_user(c, self)

        # Make sure the admin user can open up the project
        response = c.get(reverse('task_information', args=['1']))
        self.assertEqual(response.status_code, 200)
        print("Team Intern can access a task with overlapping groups")

        # # Make sure the admin user can open up the task
        #response = c.get(reverse('task_information', args=['2']))
        #self.assertEqual(response.status_code, 403)
        #print("Team Intern can NOT access a task without overlapping groups")

        c.get(reverse('logout'))

