export { keys, values, entries, size, extend } from "../core/util/object";
export * from "../core/util/array";
export * from "../core/util/string";
export * from "../core/util/random";
export * from "../core/util/types";
export * from "../core/util/eq";
import { is_NDArray, ndarray } from "../core/util/ndarray";
import { isNumber } from "../core/util/types";
import { range, linspace as _linspace } from "../core/util/array";
import { map, sum as _sum, bin_counts } from "../core/util/arrayable";
import { Random } from "../core/util/random";
import { is_equal } from "../core/util/eq";
import { float, is_Floating } from "../core/util/math";
export function is_Numerical(x) {
    return isNumber(x) || is_Floating(x) || is_NDArray(x);
}
export var np;
(function (np) {
    np.pi = Math.PI;
    function arange(start, end, step = 1) {
        const array = range(start, end, step);
        return ndarray(array, { shape: [array.length], dtype: "float64" });
    }
    np.arange = arange;
    function linspace(start, end, step) {
        const array = _linspace(start, end, step);
        return ndarray(array, { shape: [array.length], dtype: "float64" });
    }
    np.linspace = linspace;
    function mean(x) {
        return sum(x) / x.length;
    }
    np.mean = mean;
    function std(x) {
        const mu = mean(x);
        return Math.sqrt(sum(map(x, (xi) => (xi - mu) ** 2)) / x.length);
    }
    np.std = std;
    function sum(x) {
        return _sum(x);
    }
    np.sum = sum;
    function diff(x) {
        const m = x.length - 1;
        const r = new Float64Array(m);
        for (let i = 0; i < m; i++) {
            r[i] = x[i + 1] - x[i];
        }
        return ndarray(r.buffer, { shape: [m] });
    }
    np.diff = diff;
    function sin(x) {
        if (isNumber(x))
            return Math.sin(x);
        else if (is_Floating(x))
            return Math.sin(x[float]());
        else
            return map(x, (v) => Math.sin(v));
    }
    np.sin = sin;
    function cos(x) {
        if (isNumber(x))
            return Math.cos(x);
        else if (is_Floating(x))
            return Math.cos(x[float]());
        else
            return map(x, (v) => Math.cos(v));
    }
    np.cos = cos;
    function exp(x) {
        if (isNumber(x))
            return Math.exp(x);
        else if (is_Floating(x))
            return Math.exp(x[float]());
        else
            return map(x, (v) => Math.exp(v));
    }
    np.exp = exp;
    function sqrt(x) {
        if (isNumber(x))
            return Math.sqrt(x);
        else if (is_Floating(x))
            return Math.sqrt(x[float]());
        else
            return map(x, (v) => Math.sqrt(v));
    }
    np.sqrt = sqrt;
    function pos(x) {
        if (isNumber(x))
            return +x;
        else if (is_Floating(x))
            return +x[float]();
        else
            return map(x, (v) => +v);
    }
    np.pos = pos;
    function neg(x) {
        if (isNumber(x))
            return -x;
        else if (is_Floating(x))
            return -x[float]();
        else
            return map(x, (v) => -v);
    }
    np.neg = neg;
    function add(x0, y0) {
        const x = is_Floating(x0) ? x0[float]() : x0;
        const y = is_Floating(y0) ? y0[float]() : y0;
        const x_num = isNumber(x);
        const y_num = isNumber(y);
        if (x_num && y_num)
            return x + y;
        else if (x_num && !y_num)
            return map(y, (yi) => x + yi);
        else if (!x_num && y_num)
            return map(x, (xi) => xi + y);
        else if (is_NDArray(x) && is_NDArray(y)) {
            if (is_equal(x.shape, y.shape) && x.dtype == y.dtype)
                return map(x, (xi, i) => xi + y[i]);
            else
                throw new Error("shape or dtype mismatch");
        }
        else
            throw new Error("not implemented");
    }
    np.add = add;
    function sub(x0, y0) {
        const x = is_Floating(x0) ? x0[float]() : x0;
        const y = is_Floating(y0) ? y0[float]() : y0;
        const x_num = isNumber(x);
        const y_num = isNumber(y);
        if (x_num && y_num)
            return x - y;
        else if (x_num && !y_num)
            return map(y, (yi) => x - yi);
        else if (!x_num && y_num)
            return map(x, (xi) => xi - y);
        else if (is_NDArray(x) && is_NDArray(y)) {
            if (is_equal(x.shape, y.shape) && x.dtype == y.dtype)
                return map(x, (xi, i) => xi - y[i]);
            else
                throw new Error("shape or dtype mismatch");
        }
        else
            throw new Error("not implemented");
    }
    np.sub = sub;
    function mul(x0, y0) {
        const x = is_Floating(x0) ? x0[float]() : x0;
        const y = is_Floating(y0) ? y0[float]() : y0;
        const x_num = isNumber(x);
        const y_num = isNumber(y);
        if (x_num && y_num)
            return x * y;
        else if (x_num && !y_num)
            return map(y, (yi) => x * yi);
        else if (!x_num && y_num)
            return map(x, (xi) => xi * y);
        else if (is_NDArray(x) && is_NDArray(y)) {
            if (is_equal(x.shape, y.shape) && x.dtype == y.dtype)
                return map(x, (xi, i) => xi * y[i]);
            else
                throw new Error("shape or dtype mismatch");
        }
        else
            throw new Error("not implemented");
    }
    np.mul = mul;
    function div(x0, y0) {
        const x = is_Floating(x0) ? x0[float]() : x0;
        const y = is_Floating(y0) ? y0[float]() : y0;
        const x_num = isNumber(x);
        const y_num = isNumber(y);
        if (x_num && y_num)
            return x / y;
        else if (x_num && !y_num)
            return map(y, (yi) => x / yi);
        else if (!x_num && y_num)
            return map(x, (xi) => xi / y);
        else if (is_NDArray(x) && is_NDArray(y)) {
            if (is_equal(x.shape, y.shape) && x.dtype == y.dtype)
                return map(x, (xi, i) => xi / y[i]);
            else
                throw new Error("shape or dtype mismatch");
        }
        else
            throw new Error("not implemented");
    }
    np.div = div;
    function pow(x0, y0) {
        const x = is_Floating(x0) ? x0[float]() : x0;
        const y = is_Floating(y0) ? y0[float]() : y0;
        const x_num = isNumber(x);
        const y_num = isNumber(y);
        if (x_num && y_num)
            return x ** y;
        else if (x_num && !y_num)
            return map(y, (yi) => x ** yi);
        else if (!x_num && y_num)
            return map(x, (xi) => xi ** y);
        else if (is_NDArray(x) && is_NDArray(y)) {
            if (is_equal(x.shape, y.shape) && x.dtype == y.dtype)
                return map(x, (xi, i) => xi ** y[i]);
            else
                throw new Error("shape or dtype mismatch");
        }
        else
            throw new Error("not implemented");
    }
    np.pow = pow;
    function histogram(array, options) {
        const { density, bins } = options;
        const edges = ndarray(bins, { dtype: "float64", shape: [bins.length] });
        const hist = ndarray(bin_counts(array, edges), { dtype: "float64", shape: [edges.length - 1] });
        if (density) {
            const normed = div(div(hist, diff(edges)), sum(hist));
            return [normed, edges];
        }
        else
            return [hist, edges];
    }
    np.histogram = histogram;
    let random;
    (function (random) {
        class RandomGenerator {
            constructor(seed) {
                this._random = new Random(seed ?? Date.now());
            }
            normal(loc, scale, size) {
                const array = new Float64Array(size);
                const [mu, sigma] = [loc, scale];
                for (let i = 0; i < size; i += 2) {
                    // Box-Muller transform from uniform to normal distribution.
                    const u = this._random.float();
                    const v = this._random.float();
                    const common = Math.sqrt(-2.0 * Math.log(u));
                    array[i] = mu + sigma * (common * Math.cos(2.0 * np.pi * v));
                    if (i + 1 < size)
                        array[i + 1] = mu + sigma * (common * Math.sin(2.0 * np.pi * v));
                }
                return ndarray(array.buffer, { shape: [size], dtype: "float64" });
            }
        }
        RandomGenerator.__name__ = "RandomGenerator";
        random.RandomGenerator = RandomGenerator;
        function default_rng(seed) {
            return new RandomGenerator(seed);
        }
        random.default_rng = default_rng;
    })(random = np.random || (np.random = {}));
})(np || (np = {}));
//# sourceMappingURL=linalg.js.map