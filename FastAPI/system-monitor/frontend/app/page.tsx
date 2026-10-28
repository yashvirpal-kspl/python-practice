import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { COOKIE } from "@/lib/server";

export default async function Home() {
  const signedIn = Boolean((await cookies()).get(COOKIE)?.value);
  redirect(signedIn ? "/dashboard" : "/login");
}
