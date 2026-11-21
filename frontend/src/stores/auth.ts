import { defineStore } from "pinia";
import api from "@/api";

interface User {
  username: string;
  email: string;
  id: number;
  is_active: boolean;
  created_at: string;
  roles: string[];
}

interface CSRFResponse {
  response: { csrf_token: string };
}

interface AuthTokenReponse {
  response: {
    user: { authentication_token: string };
  };
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    csrfToken: null as string | null,
    accessToken: null as string | null,
    user: null as User | null,
    ready: false,
  }),
  getters: {
    isAuthenticated: (s): boolean => !!s.accessToken,
  },
  actions: {
    async getCSRFToken() {
      this.csrfToken = (
        await api.get<CSRFResponse>("/backend/login")
      ).response.csrf_token;
    },
    async login(
      email: string | null,
      username: string | null,
      password: string,
    ) {
      if (!email && !username) {
        throw new Error("Either email or username must be provided");
      }

      await this.getCSRFToken();
      const data = await api.post<AuthTokenReponse & CSRFResponse>(
        "/backend/login?include_auth_token",
        { email, username, password, csrf_token: this.csrfToken },
      );
      this.accessToken = data.response.user.authentication_token;
      this.user = await api.get("/backend/api/user/profile");
    },
    async register(email: string, username: string, password: string) {
      await this.getCSRFToken();
      await api.post<AuthTokenReponse & CSRFResponse>("/backend/register", {
        email,
        username,
        password,
        password_confirm: password,
        csrf_token: this.csrfToken,
      });
    },
    async refresh(): Promise<string> {
      if (!this.csrfToken) {
        await this.getCSRFToken();
      }
      const data = await api.post<AuthTokenReponse>("/backend/refresh-token", {
        csrf_token: this.csrfToken,
      });
      this.accessToken = data.response.user.authentication_token;
      this.user = await api.get("/backend/api/user/profile");
      return this.accessToken;
    },
    async restoreSession() {
      try {
        await this.refresh();
      } catch {
        /* not logged in */
      }
      this.ready = true;
    },
    async logout() {
      try {
        await api.post("/backend/logout");
      } finally {
        this.accessToken = null;
        this.user = null;
      }
    },
  },
});
