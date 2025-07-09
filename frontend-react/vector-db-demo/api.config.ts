import { Options } from "orval";

const API_PATH = "./src/api";

export const config: Options = {
    input: "./src/schema/vector-db-demo-schema.json",
    output: {
        target: `${API_PATH}/generated/vector-db-demo.ts`,
        mode: "tags-split",
        client: "react-query",
        mock: false,
        clean: true,
        prettier: true,
        tslint: true,
        override: {
            mutator: {
                path: './src/api/axios-client.ts',
                name: 'axiosClient',
            },
        },
    },
};
