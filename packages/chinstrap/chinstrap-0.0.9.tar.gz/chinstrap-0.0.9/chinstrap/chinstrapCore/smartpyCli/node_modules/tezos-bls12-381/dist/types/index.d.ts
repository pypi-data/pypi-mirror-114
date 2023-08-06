declare const Bls12: {
    addG1: (byteString1: string, byteString2: string) => string;
    addG2: (byteString1: string, byteString2: string) => string;
    addFr: (byteString1: string, byteString2: string) => string;
    multiplyG1ByFr: (byteString1: string, byteString2: string) => string;
    multiplyG2ByFr: (byteString1: string, byteString2: string) => string;
    multiplyFrByFr: (byteString1: string, byteString2: string) => string;
    multiplyFrByInt: (byteString: string, int: string | number) => string;
    negateG1: (byteString: string) => string;
    negateG2: (byteString: string) => string;
    negateFr: (byteString: string) => string;
    convertFrToInt: (byteString: string) => string;
    pairingCheck: (list: string[][]) => boolean;
};
export default Bls12;
