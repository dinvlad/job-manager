/**
 * Job Manager Service
 * Job Manager API for interacting with asynchronous batch jobs and workflows.
 *
 * OpenAPI spec version: 0.0.1
 *
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the class manually.
 */

import * as models from './models';

/**
 * Job and task level metadata
 */
export interface JobMetadataResponse {
    /**
     * The identifier of the job
     */
    id: string;

    status: models.JobStatus;

    /**
     * Submission datetime of the job in ISO8601 format
     */
    submission: Date;

    /**
     * The name of the job
     */
    name?: string;

    /**
     * Start datetime of the job in ISO8601 format
     */
    start?: Date;

    /**
     * End datetime of the job in ISO8601 format
     */
    end?: Date;

    /**
     * Map of input keys to input values
     */
    inputs?: any;

    /**
     * Map of output keys to output values
     */
    outputs?: any;

    /**
     * Custom job labels with string values
     */
    labels?: any;

    /**
     * Map of type of log file to its location
     */
    logs?: any;

    tasks?: Array<models.TaskMetadata>;

    failures?: Array<models.FailureMessage>;

}
