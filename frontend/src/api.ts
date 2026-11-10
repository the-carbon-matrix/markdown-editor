import { useAuthStore } from "@/stores/auth";
import router from "./router";

interface RequestOptions {
  method: string;
  body?: unknown;
  headers?: HeadersInit;
}

const AUTH_PATHS = ["/login", "/logout", "/register", "/refresh-token"];

const send = (
  path: string,
  {
    method = "GET",
    body,
    headers: extraHeaders,
    token,
    ...rest
  }: RequestOptions & { token?: string | null },
): Promise<Response> => {
  const headers = new Headers(extraHeaders);
  headers.set("Accept", "application/json");

  const init: RequestInit = {
    method,
    credentials: "include",
    headers,
    body: null as string | null,
    ...rest,
  };

  if (body !== undefined) {
    headers.set("Content-Type", "application/json");
    init.body = JSON.stringify(body);
  }

  if (token) {
    headers.set("Authentication-Token", token);
  }

  return fetch(`${path}`, init);
};

async function parseBody(res: Response): Promise<unknown> {
  if (res.status === 204) return null;
  const text = await res.text();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

let refreshPromise: Promise<string> | null = null;

const request = async <T,>(
  path: string,
  options: RequestOptions,
  retried = false,
): Promise<T> => {
  const auth = useAuthStore();
  const res = await send(path, { ...options, token: auth.accessToken });

  const isAuthRoute: boolean = AUTH_PATHS.some((p) => path.startsWith(p));

  if (res.status === 401 && !retried && !isAuthRoute) {
    try {
      refreshPromise ??= auth.refresh().finally(() => {
        refreshPromise = null;
      });
      await refreshPromise;
    } catch {
      auth.accessToken = null;
      auth.user = null;
      router.push({
        name: "login",
        query: { redirect: router.currentRoute.value.fullPath },
      });
      throw new Error("Error 401: Failed to authenticate!");
    }
    return request<T>(path, options, true);
  }

  const data = await parseBody(res);
  if (!res.ok) {
    console.log(data);
    throw new Error(`Error ${res.status}: ${data}`);
  }
  return data as T;
};

const api = {
  get: <T = unknown,>(path: string, opts?: RequestOptions) =>
    request<T>(path, { ...opts, method: "GET" }),
  post: <T = unknown,>(path: string, body?: unknown, opts?: RequestOptions) =>
    request<T>(path, { ...opts, method: "POST", body }),
  put: <T = unknown,>(path: string, body?: unknown, opts?: RequestOptions) =>
    request<T>(path, { ...opts, method: "PUT", body }),
  patch: <T = unknown,>(path: string, body?: unknown, opts?: RequestOptions) =>
    request<T>(path, { ...opts, method: "PATCH", body }),
  delete: <T = unknown,>(path: string, opts?: RequestOptions) =>
    request<T>(path, { ...opts, method: "DELETE" }),
};

export default api;
