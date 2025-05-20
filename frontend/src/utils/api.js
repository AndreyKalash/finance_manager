import { RTYPES } from "./recordTypes"

export const pathBilder = (type, path, expensePath, incomePath) => {
  return path + (
      type == RTYPES.expense ?
      expensePath :
      incomePath
    )
} 
