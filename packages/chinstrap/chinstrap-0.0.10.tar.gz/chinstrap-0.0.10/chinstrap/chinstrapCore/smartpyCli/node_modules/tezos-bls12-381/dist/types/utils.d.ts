import { Fr } from 'noble-bls12-381';
/**
 * @description Convert hexadecimal to a Prime Field.
 *
 * @param {string} byteString
 *
 * @return {Fr} Prime Field
 */
export declare const frOfHex: (byteString: string) => Fr;
/**
 * @description Convert hexadecimal big endian to little endian.
 *
 * @param {string} byteString - e.g. 000000000000000000000000000000000000000000000000000126ad20e84000
 *
 * @return {string} - e.g. 0040e820ad260100000000000000000000000000000000000000000000000000
 */
export declare const bigEndianToLittleEndian: (byteString: string) => string;
/**
 * @description Convert hexadecimal to big int.
 *
 * @param {string} byteString
 *
 * @return {bigint}
 */
export declare const bigIntOfHex: (hex: string) => bigint;
