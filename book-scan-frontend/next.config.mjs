import MillionLint from '@million/lint';
/** @type {import('next').NextConfig} */
const nextConfig = {};

export default MillionLint.next(
  nextConfig, { rsc: true }
);
