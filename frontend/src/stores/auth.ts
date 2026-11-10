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
    async login(email: string, username: string, password: string) {
      this.csrfToken = (
        await api.get<CSRFResponse>("/login")
      ).response.csrf_token;
      const data = await api.post<AuthTokenReponse & CSRFResponse>(
        "/login?include_auth_token",
        { email, username, password, csrf_token: this.csrfToken },
      );
      this.accessToken = data.response.user.authentication_token;
      this.user = await api.get("/api/user/profile");
    },
    async refresh(): Promise<string> {
      const data = await api.post<AuthTokenReponse>("/refresh-token", {
        csrf_token: this.csrfToken,
      });
      this.accessToken = data.response.user.authentication_token;
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
        await api.post("/logout");
      } finally {
        this.accessToken = null;
        this.user = null;
      }
    },
  },
});
