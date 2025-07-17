import { esbuildPlugin } from '@web/dev-server-esbuild';

/**
 * @type {import('@web/dev-server').DevServerConfig}
 */
export default {
  // TODO: importmaps
  nodeResolve: true,
  middleware: [
    /**
     * CORS middleware
     * @param ctx koa context
     * @param next middleware
     */
    function cors(ctx, next) {
      ctx.set('Access-Control-Allow-Origin', 'http://localhost:8000 http://localhost:8001');
      return next();
    }
  ],
  plugins: [
    // serve typescript sources as javascript
    esbuildPlugin({
      ts: true,
      tsconfig: 'tsconfig.json',
    }),
  ],
};
