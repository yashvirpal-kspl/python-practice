/** @type {import('next').NextConfig} */
const nextConfig = {
  poweredByHeader: false,
  output: "standalone", // small self-contained server for the Docker image
};

export default nextConfig;
