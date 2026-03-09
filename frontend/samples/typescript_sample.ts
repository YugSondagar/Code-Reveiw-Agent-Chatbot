/**
 * Advanced Data Processing Pipeline with TypeScript
 */

interface DataSource<T> {
    getData(): Promise<T[]>;
    getById(id: string): Promise<T | null>;
}

interface DataTransformer<I, O> {
    transform(input: I[]): O[];
}

interface DataValidator<T> {
    validate(item: T): boolean;
    getErrors(item: T): string[];
}

interface DataProcessor<T> {
    process(item: T): Promise<T>;
    processBatch(items: T[]): Promise<T[]>;
}

class ApiDataSource<T extends { id: string }> implements DataSource<T> {
    constructor(
        private baseUrl: string,
        private headers: Record<string, string> = {}
    ) {}

    async getData(): Promise<T[]> {
        try {
            const response = await fetch(this.baseUrl, {
                headers: this.headers
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data as T[];
        } catch (error) {
            console.error('Failed to fetch data:', error);
            throw error;
        }
    }

    async getById(id: string): Promise<T | null> {
        try {
            const response = await fetch(`${this.baseUrl}/${id}`, {
                headers: this.headers
            });

            if (response.status === 404) {
                return null;
            }

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data as T;
        } catch (error) {
            console.error(`Failed to fetch item ${id}:`, error);
            throw error;
        }
    }
}

class UserValidator implements DataValidator<User> {
    validate(user: User): boolean {
        return this.getErrors(user).length === 0;
    }

    getErrors(user: User): string[] {
        const errors: string[] = [];

        if (!user.email || !this.isValidEmail(user.email)) {
            errors.push('Invalid email address');
        }

        if (!user.name || user.name.trim().length < 2) {
            errors.push('Name must be at least 2 characters');
        }

        if (user.age !== undefined && (user.age < 0 || user.age > 150)) {
            errors.push('Age must be between 0 and 150');
        }

        return errors;
    }

    private isValidEmail(email: string): boolean {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
}

class UserTransformer implements DataTransformer<any, User> {
    transform(input: any[]): User[] {
        return input
            .map(item => this.transformUser(item))
            .filter((user): user is User => user !== null);
    }

    private transformUser(data: any): User | null {
        try {
            return {
                id: data.id || crypto.randomUUID(),
                name: data.name || data.username || 'Unknown',
                email: data.email || '',
                age: data.age ? parseInt(data.age) : undefined,
                createdAt: data.createdAt ? new Date(data.createdAt) : new Date(),
                isActive: data.isActive ?? true
            };
        } catch {
            return null;
        }
    }
}

class BatchProcessor<T> implements DataProcessor<T> {
    private validators: DataValidator<T>[] = [];
    private transformers: DataTransformer<T, T>[] = [];

    constructor(
        private batchSize: number = 100,
        private concurrency: number = 5
    ) {}

    addValidator(validator: DataValidator<T>): void {
        this.validators.push(validator);
    }

    addTransformer(transformer: DataTransformer<T, T>): void {
        this.transformers.push(transformer);
    }

    async process(item: T): Promise<T> {
        // Validate item
        for (const validator of this.validators) {
            if (!validator.validate(item)) {
                const errors = validator.getErrors(item);
                throw new Error(`Validation failed: ${errors.join(', ')}`);
            }
        }

        // Apply transformations
        let processedItem = item;
        for (const transformer of this.transformers) {
            const transformed = transformer.transform([processedItem]);
            if (transformed.length > 0) {
                processedItem = transformed[0];
            }
        }

        return processedItem;
    }

    async processBatch(items: T[]): Promise<T[]> {
        const results: T[] = [];
        
        // Process in batches
        for (let i = 0; i < items.length; i += this.batchSize) {
            const batch = items.slice(i, i + this.batchSize);
            
            // Process batch with concurrency limit
            const batchPromises = batch.map(item => this.process(item));
            const batchResults = await Promise.all(batchPromises);
            
            results.push(...batchResults);
        }

        return results;
    }
}

// Type definitions
interface User {
    id: string;
    name: string;
    email: string;
    age?: number;
    createdAt: Date;
    isActive: boolean;
}

// Usage example
async function main() {
    // Setup pipeline
    const source = new ApiDataSource<User>('https://api.example.com/users');
    const validator = new UserValidator();
    const transformer = new UserTransformer();
    const processor = new BatchProcessor<User>(50, 3);

    processor.addValidator(validator);

    try {
        // Fetch data
        const rawData = await source.getData();
        console.log(`Fetched ${rawData.length} users`);

        // Transform data
        const users = transformer.transform(rawData);
        console.log(`Transformed ${users.length} users`);

        // Process users
        const processed = await processor.processBatch(users);
        console.log(`Successfully processed ${processed.length} users`);

        // Get specific user
        const user = await source.getById('123');
        if (user) {
            const result = await processor.process(user);
            console.log('Processed user:', result);
        }

    } catch (error) {
        console.error('Pipeline failed:', error);
    }
}

// Run the example
main().catch(console.error);