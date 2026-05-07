from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse


class AuthRouteSmokeTests(TestCase):
    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_staff_login_page_loads(self):
        response = self.client.get(reverse('staff_login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page_loads(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_creates_user_and_redirects(self):
        response = self.client.post(
            reverse('signup'),
            data={
                'username': 'newuser',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.filter(username='newuser').count(), 1)


class HealthEndpointTests(TestCase):
    def test_health_json(self):
        response = self.client.get(f"{reverse('health')}?format=json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')
        self.assertEqual(response.json()['service'], 'kistie-store')


class CatalogRedirectTests(TestCase):
    def test_catalog_redirects_to_inventory(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 302)
        location = response.headers.get('Location', '')
        self.assertTrue(location.endswith(reverse('inventory')))

    def test_catalog_redirect_preserves_querystring(self):
        response = self.client.get(reverse('catalog'), {'category': '1', 'currency': 'EUR'})
        self.assertEqual(response.status_code, 302)
        location = response.headers.get('Location', '')
        self.assertIn('/inventory/', location)
        self.assertIn('category=1', location)
        self.assertIn('currency=EUR', location)


class StaffDashboardPermissionTests(TestCase):
    """Staff dashboard uses ``access_staff_dashboard`` — not Django ``is_staff`` (admin login)."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.perm = Permission.objects.get(
            content_type__app_label='core',
            codename='access_staff_dashboard',
        )
        cls.shop_staff = User.objects.create_user('portal_staff', password='StrongPortalStaff123!')
        cls.shop_staff.user_permissions.add(cls.perm)
        cls.superuser = User.objects.create_superuser(
            'portal_super',
            'portal_super@test.example',
            'StrongPortalSu123!',
        )
        cls.regular = User.objects.create_user('portal_buyer', password='StrongBuyer123!')

    def test_staff_dashboard_redirects_when_anonymous(self):
        response = self.client.get(reverse('staff_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_staff_dashboard_forbidden_without_permission(self):
        self.client.force_login(self.regular)
        response = self.client.get(reverse('staff_dashboard'))
        self.assertEqual(response.status_code, 403)

    def test_staff_dashboard_ok_with_permission_not_admin_staff_flag(self):
        self.assertFalse(self.shop_staff.is_staff)
        self.client.force_login(self.shop_staff)
        response = self.client.get(reverse('staff_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_staff_dashboard_ok_for_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse('staff_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_staff_login_redirects_portal_user_to_dashboard(self):
        response = self.client.post(
            reverse('staff_login'),
            {'username': 'portal_staff', 'password': 'StrongPortalStaff123!'},
        )
        self.assertRedirects(response, reverse('staff_dashboard'), fetch_redirect_response=False)
        self.assertIsNotNone(self.client.session.get('_auth_user_id'))

    def test_staff_login_rejects_shopper_without_logging_in(self):
        response = self.client.post(
            reverse('staff_login'),
            {'username': 'portal_buyer', 'password': 'StrongBuyer123!'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.client.session.get('_auth_user_id'))

    def test_staff_login_skipped_when_already_portal_user(self):
        self.client.force_login(self.shop_staff)
        response = self.client.get(reverse('staff_login'))
        self.assertRedirects(response, reverse('staff_dashboard'), fetch_redirect_response=False)


class AdminSuperuserOnlyMiddlewareTests(TestCase):
    """Non-superusers must not use ``/admin/`` even if ``is_staff`` or portal permission."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.regular = User.objects.create_user('adm_gate_buyer', password='StrongBuyerGate123!')
        perm = Permission.objects.get(
            content_type__app_label='core',
            codename='access_staff_dashboard',
        )
        cls.portal_only = User.objects.create_user('adm_gate_portal', password='StrongPortalGate123!')
        cls.portal_only.user_permissions.add(perm)
        cls.django_staff = User.objects.create_user(
            'adm_gate_django_staff',
            password='StrongStaffGate123!',
            is_staff=True,
        )
        cls.superuser = User.objects.create_superuser(
            'adm_gate_super',
            'adm_gate_super@test.example',
            'StrongSuperGate123!',
        )

    def test_anonymous_admin_request_not_blocked_by_middleware(self):
        response = self.client.get('/admin/')
        self.assertIn(response.status_code, (301, 302))

    def test_portal_staff_get_admin_forbidden(self):
        self.client.force_login(self.portal_only)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 403)

    def test_is_staff_user_get_admin_forbidden(self):
        self.client.force_login(self.django_staff)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 403)

    def test_superuser_admin_allowed(self):
        self.client.force_login(self.superuser)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
