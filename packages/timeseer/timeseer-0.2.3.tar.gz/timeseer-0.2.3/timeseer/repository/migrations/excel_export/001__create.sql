create table ExcelExporterRuns (
    id integer primary key autoincrement,
    excel_export_id int not null,
    state text not null,

    unique(excel_export_id)
);

create table ExcelExport (
    id integer primary key autoincrement,
    filename text,
    file blob,
    date datetime
);

create table Series_ExcelExport (
    id integer primary key autoincrement,
    excel_export_id not null,
    series_source text not null,
    series_id text not null,

    foreign key (excel_export_id) references ExcelExport(id) on delete cascade
);
