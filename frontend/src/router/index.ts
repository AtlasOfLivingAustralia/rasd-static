import { createRouter, createWebHashHistory } from 'vue-router';
import HomeView from '@/views/HomepageView.vue';
import AddOrganisationView from '@/views/AddOrganisationView.vue';
import OrganisationListView from '@/views/OrganisationListView.vue';
import OrganisationView from '../views/OrganisationView.vue';
import MetadataView from '@/views/MetadataView.vue';
import AddMetadataView from '@/views/AddMetadataView.vue';
import LoginView from '@/views/LoginView.vue';
import RegisterLandingPageView from '../views/RegisterLandingPageView.vue';
import CreatePasswordView from '@/views/CreatePasswordView.vue';
import ToolsView from '@/views/ToolsView.vue';
import ForgotPasswordView from '@/views/ForgotPasswordView.vue';
import ConfirmForgotPasswordView from '@/views/ConfirmForgotPassword.vue';
import SearchView from '@/views/SearchView.vue';
import MetadataListView from '@/views/MetadataListView.vue';
import PrivacyNoticeView from '@/views/PrivacyNoticeView.vue';
import TermsOfUseView from '@/views/TermsOfUseView.vue';
import RegisterView from '@/views/RegisterView.vue';
import AssessRegistrationRequests from '@/views/AssessRegistrationRequests.vue';
import DataAccessRequest from '@/views/DataAccessRequest.vue';
import DataAccessRequestAction from '@/views/DataAccessRequestAction.vue';
import { UserGroup } from '@/api/api.types';

import { useUserDataStore } from '@/store';
import { useProgrammatic } from '@oruga-ui/oruga-next';
import PublicDARView from '@/views/PublicDARView.vue';

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterLandingPageView,
    },
    {
      path: '/create-password',
      name: 'create-password',
      component: CreatePasswordView,
    },
    {
      path: '/tools',
      name: 'tools',
      component: ToolsView,
      // Ommitted 'meta: { requiresLogin: true}' as it blocks login flow. Auth check for tools page is handled on the page.
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: ForgotPasswordView,
    },
    {
      path: '/forgot-password/confirm',
      name: 'forgot-password/confirm',
      component: ConfirmForgotPasswordView,
      meta: { username: 'username' },
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/organisations/add',
      name: 'add-organisation',
      component: AddOrganisationView,
      meta: { requiresLogin: true, requiresAdmin: true },
    },
    {
      path: '/organisations',
      name: 'organisations',
      component: OrganisationListView,
      meta: { requiresLogin: true, requiresAdmin: true },
    },
    {
      path: '/organisations/:id',
      name: 'organisation',
      component: OrganisationView,
      meta: { requiresLogin: true, requiresAdmin: true },
    },
    {
      path: '/metadata/:id',
      name: 'metadata-view',
      component: MetadataView,
      meta: { requiresLogin: true, requiresDataCustodian: true },
    },
    {
      path: '/metadata/add',
      name: 'add-metadata',
      component: AddMetadataView,
      meta: { requiresLogin: true, requiresDataCustodian: true },
    },
    {
      path: '/metadata',
      name: 'metadata-list',
      component: MetadataListView,
      meta: { requiresLogin: true, requiresDataCustodian: true },
    },
    {
      path: '/privacy-notice',
      name: 'privacy-notice',
      component: PrivacyNoticeView,
    },
    {
      path: '/terms-of-use',
      name: 'terms-of-use',
      component: TermsOfUseView,
    },
    {
      path: '/register/data-custodian',
      name: 'register-data-custodian',
      component: RegisterView,
      props: { role: 'DataCustodians' },
    },
    {
      path: '/register/data-requestor',
      name: 'register-data-requestor',
      component: RegisterView,
      props: { role: 'DataRequestors' },
    },
    {
      path: '/registrations/registration-requests',
      name: 'assess-organisation-requests',
      component: AssessRegistrationRequests,
      meta: { requiresLogin: true, requiresAdmin: true },
    },
    {
      path: '/data-access-request',
      name: 'data-access-request',
      component: DataAccessRequest,
      meta: { requiresLogin: true },
    },
    {
      path: '/data-access-request/view',
      name: 'data-access-request-view',
      component: DataAccessRequestAction,
      meta: { requiresLogin: true },
      props: { role: UserGroup.DataRequestors },
    },
    {
      path: '/data-access-request/edit',
      name: 'data-access-request-edit',
      component: DataAccessRequestAction,
      meta: { requiresLogin: true, requiresDataCustodian: true },
      props: { role: UserGroup.DataCustodians },
    },
    {
      path: '/data-access-request/admin',
      name: 'data-access-request-admin',
      component: DataAccessRequestAction,
      meta: { requiresLogin: true, requiresAdmin: true },
      props: { role: UserGroup.Administrators },
    },
    {
      path: '/data-access-request/public/:id',
      name: 'data-access-request-public',
      component: PublicDARView,
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
});

function notifyUnauthorisedAccess(oruga: any) {
  oruga.notification.open({
    variant: 'danger',
    message: 'You are not authorised to access this page.',
    position: 'top',
    duration: 5000,
    closable: true,
  });
}

router.beforeEach((to, from, next) => {
  const { oruga } = useProgrammatic();
  const userDataStore = useUserDataStore();
  const isLoggedIn = userDataStore.isLoggedIn;
  const userGroup = userDataStore.groups ? userDataStore.groups[0] : undefined;
  if (
    (to.meta.requiresLogin && !isLoggedIn) ||
    (to.meta.requiresAdmin && userGroup !== 'Administrators') ||
    (to.meta.requiresDataCustodian && userGroup !== 'Administrators' && userGroup !== 'DataCustodians')
  ) {
    notifyUnauthorisedAccess(oruga);
    next({
      path: '/login',
    });
  } else {
    next();
  }
});

export default router;
