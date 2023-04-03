import jwt from "jsonwebtoken";
import prisma from "./prisma";

export function generateAccessToken(username, email) {
  return jwt.sign(
    {user: username, email: email},
    process.env.SECRET_TOKEN,
    {
      expiresIn: '1h',
    }
  );
}

export function generateRefreshToken(username, email) {
  return jwt.sign(
    {user: username, email: email},
    process.env.SECRET_RTOKEN,
    {
      expiresIn: '30d',
    }
  )
}

export async function addToList(user, refresher) {
  try {
    await prisma.token.create({
      // data: {
        
      // },
    });
  } catch(error) {
    console.log(error);
  }
}
