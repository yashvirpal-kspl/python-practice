import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import Dashboard from "@/components/Dashboard";
import { COOKIE } from "@/lib/server";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  // A revoked or invalid key is handled client-side: the first API call returns 401 and redirects to /login
  if (!(await cookies()).get(COOKIE)?.value) redirect("/login");
  return <Dashboard />;
}
