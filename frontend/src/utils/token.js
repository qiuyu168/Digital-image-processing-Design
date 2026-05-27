export const generateTestToken = (payload) => {
    const header = {
        alg: 'HS256',
        typ: 'JWT'
    };

    const base64URLEncode = (obj) => {
        return btoa(encodeURIComponent(JSON.stringify(obj)))
          .replace(/\+/g, '-') // 替换为标准 Base64URL 字符
          .replace(/\//g, '_')
          .replace(/=+$/, ''); // 去除末尾等号
    };

    const encodedHeader = base64URLEncode(header);
    const encodedPayload = base64URLEncode(payload);

    const signature = btoa('local_test_signature_' + encodedPayload.slice(0, 8))
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/, '');

    return `${encodedHeader}.${encodedPayload}.${signature}`;
}