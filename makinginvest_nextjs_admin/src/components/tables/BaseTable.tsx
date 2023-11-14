import { ActionIcon, Box, Select, Text, TextInput } from '@mantine/core';
import { IconChevronLeft, IconChevronRight } from '@tabler/icons';
import { RankingInfo, rankItem } from '@tanstack/match-sorter-utils';
import {
  ColumnDef,
  FilterFn,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  HeaderGroup,
  PaginationState,
  Row,
  SortingState,
  useReactTable
} from '@tanstack/react-table';
import React from 'react';
import { ArrowDown, ArrowRight, ArrowUp } from 'tabler-icons-react';

declare module '@tanstack/table-core' {
  interface FilterMeta {
    itemRank: RankingInfo;
  }
}

export type IBaseTableProps = {
  columns: ColumnDef<any, any>[];
  data: any[];
};

const fuzzyFilter: FilterFn<any> = (row, columnId, value, addMeta) => {
  const itemRank = rankItem(row.getValue(columnId), value);
  addMeta({ itemRank });
  return itemRank.passed;
};

export function BaseTable({ columns, data }: IBaseTableProps) {
  const [pagination, setPagination] = React.useState<PaginationState>({ pageIndex: 0, pageSize: 10 });
  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [globalFilter, setGlobalFilter] = React.useState('');

  const instance = useReactTable({
    data,
    columns,
    state: { sorting, pagination, globalFilter },
    globalFilterFn: fuzzyFilter,
    onGlobalFilterChange: setGlobalFilter,
    onSortingChange: setSorting,
    onPaginationChange: setPagination,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel()
  });

  return (
    <>
      <div className='border rounded shadow-md border-slate-300 border-opacity-30 text-[12px]'>
        <div className='mx-2 mt-2'>
          <TextInput
            className='mt-6'
            placeholder='Type a keyword to search...'
            type='text'
            value={globalFilter ?? ''}
            onChange={(e) => setGlobalFilter(String(e.target.value))}
          />
        </div>
        <div className='overflow-auto'>
          <table className='min-w-[1000px] w-full border-transparent'>
            <thead className=''>
              {instance.getHeaderGroups().map((headerGroup: HeaderGroup<any>) => (
                <tr className='p-0 m-0 border-none' key={headerGroup.id}>
                  {headerGroup.headers.map((header) => (
                    <th
                      style={{ width: header.getSize() !== 150 ? header.getSize() : undefined }}
                      key={header.id}
                      className={`w-[${header.getSize()}%]  dark:border-gray-700 text-left py-3 px-2 bg-slate-100 dark:bg-gray-800  text-gray-600 dark:text-gray-300  font-bold`}>
                      {header.isPlaceholder ? null : (
                        <div
                          {...{
                            className: header.column.getCanSort() ? 'cursor-pointer select-none flex items-center align-middle' : 'flex',
                            onClick: header.column.getToggleSortingHandler()
                          }}>
                          {flexRender(header.column.columnDef.header, header.getContext())}
                          {{
                            asc: <ArrowUp className='ml-1' />,
                            desc: <ArrowDown className='ml-1' />
                          }[header.column.getIsSorted() as string] ?? <ArrowRight className='ml-1 text-transparent' />}
                        </div>
                      )}
                    </th>
                  ))}
                </tr>
              ))}
            </thead>

            {/* Cells */}
            <tbody>
              {instance.getRowModel().rows.map((row: Row<any>) => (
                <tr key={row.id} className='transition hover:bg-slate-50 hover hover:dark:bg-dark-400'>
                  {row.getVisibleCells().map((cell) => (
                    <td className='text-left text-[13.5px] py-4 px-2 border-b border-gray-100 dark:border-gray-700' key={cell.id}>
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* pagination */}
        <div className='flex items-center justify-end gap-2 px-4 py-3'>
          <Box className='flex items-center mr-0'>
            <Text className='mr-2'>Rows per page</Text>
            <Select
              className='w-[70px] p-0 mb-0 native-select-table'
              iconWidth={0}
              placeholder='10'
              value={pagination.pageSize.toString()}
              onChange={(e) => {
                instance.setPageSize(Number(e));
              }}
              data={[
                { value: '10', label: '10' },
                { value: '20', label: '20' },
                { value: '30', label: '30' },
                { value: '40', label: '40' },
                { value: '50', label: '50' }
              ]}
            />
          </Box>

          <span className='flex items-center gap-1 mr-4'>
            <div>Page</div>
            <Text>
              {instance.getState().pagination.pageIndex + 1} of {instance.getPageCount()}
            </Text>
          </span>

          <Box className='flex'>
            <ActionIcon className='mr-2' variant='subtle' onClick={() => instance.previousPage()} disabled={!instance.getCanPreviousPage()}>
              <IconChevronLeft size={30} />
            </ActionIcon>
            <ActionIcon variant='subtle' onClick={() => instance.nextPage()} disabled={!instance.getCanNextPage()}>
              <IconChevronRight size={30} />
            </ActionIcon>
          </Box>
        </div>
      </div>
    </>
  );
}
