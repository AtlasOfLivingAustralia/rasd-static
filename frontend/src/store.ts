import { defineStore } from 'pinia';
import type { ApiResponse, WhoAmIData, OrganisationState } from '@/api/api.types';
import { getOrganisationAPI, removeAuthHeader, whoAmIAPI } from '@/api/api';

export interface UserData {
  idToken: string | null;
  id: string | null;
  email: string | null;
  familyName: string | null;
  givenName: string | null;
  groups: string[] | null;
  organisationId: string | null;
  organisationName: string | null;
  organisationABN: string | null;
  organisationEmail: string | null;
}

const defaultUserDataState: UserData = {
  idToken: null,
  id: null,
  email: null,
  familyName: null,
  givenName: null,
  groups: null,
  organisationId: null,
  organisationName: null,
  organisationABN: null,
  organisationEmail: null,
};

export const useUserDataStore = defineStore('userData', {
  state: (): UserData => ({ ...defaultUserDataState }),
  actions: {
    setIdToken(token: string): void {
      this.idToken = token;
    },
    setFromWhoAmI(whoAmIData: WhoAmIData): void {
      this.id = whoAmIData.id;
      this.email = whoAmIData.email;
      this.familyName = whoAmIData.familyName;
      this.givenName = whoAmIData.givenName;
      this.groups = whoAmIData.groups;
      this.organisationId = whoAmIData.organisationId;
    },
    setUserOrganisationDetails(organisation: OrganisationState): void {
      this.organisationName = organisation.name;
      this.organisationABN = organisation.abn;
      this.organisationEmail = organisation.email;
    },
    clear(): void {
      Object.assign(this, defaultUserDataState);
    },
  },
  getters: {
    isLoggedIn: (state) => !!state.idToken,
  },
  persist: {
    storage: sessionStorage,
  },
});

export function isLoggedIn(): boolean {
  const userStore = useUserDataStore();
  return userStore.isLoggedIn;
}

export async function fetchUserData(): Promise<void> {
  const store = useUserDataStore();
  if (!store.isLoggedIn) {
    throw new Error('User is not logged-in');
  } else {
    // fetch data from whoAmI endpoint
    const apiResponse: ApiResponse<WhoAmIData> = await whoAmIAPI();
    if (!apiResponse.error && apiResponse.data) {
      store.setFromWhoAmI(apiResponse.data);
      // fetch organisation details
      const organisationDetails = await getOrganisationAPI(apiResponse.data.organisationId);
      if (organisationDetails) {
        store.setUserOrganisationDetails(organisationDetails);
      } else {
        throw new Error('Unable to retrieve user organisation details.');
      }
    } else {
      throw new Error('Unable to retrieve user details.');
    }
  }
}

export function logOutAndClearUserData(): void {
  const userDataStore = useUserDataStore();
  userDataStore.clear();
  removeAuthHeader();
}
